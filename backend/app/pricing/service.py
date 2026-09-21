"""AquaSwift — PricingService — SOLE PRICING AUTHORITY"""
from __future__ import annotations
import uuid
from datetime import datetime, timezone
from decimal import Decimal
import structlog
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.catalog.models import WaterVariant
from app.core.audit import audit_log
from app.core.exceptions import NotFoundError, ValidationError
from app.pricing.models import DeliveryPricingRule, PricingRule
from app.pricing.schemas import PricingRuleCreate, PricingRuleUpdate, QuoteResponse

logger = structlog.get_logger()
TAX_RATE = Decimal("0.18")  # 18% GST


async def quote(db: AsyncSession, variant_id: uuid.UUID, quantity_litres: int,
                customer_type: str = "INDIVIDUAL") -> QuoteResponse:
    """
    PricingService.quote() — the SOLE pricing authority (RULE-005).
    All price calculations MUST go through this function.
    """
    variant = await db.get(WaterVariant, variant_id)
    if not variant or not variant.is_active:
        raise NotFoundError("WaterVariant", variant_id)

    if quantity_litres < variant.min_quantity_litres or quantity_litres > variant.max_quantity_litres:
        raise ValidationError(code="QUANTITY_OUT_OF_RANGE",
                              message=f"Quantity must be between {variant.min_quantity_litres} and {variant.max_quantity_litres} litres.")

    # Find matching pricing rule
    now = datetime.now(timezone.utc)
    result = await db.execute(
        select(PricingRule)
        .where(PricingRule.is_active == True, PricingRule.active_from <= now)
        .where((PricingRule.active_to == None) | (PricingRule.active_to > now))
        .where((PricingRule.purpose_id == variant.purpose_id) | (PricingRule.purpose_id == None))
        .where((PricingRule.quality_id == variant.quality_id) | (PricingRule.quality_id == None))
        .where((PricingRule.customer_type == customer_type) | (PricingRule.customer_type == None))
        .order_by(PricingRule.purpose_id.desc().nullslast(), PricingRule.quality_id.desc().nullslast(),
                  PricingRule.customer_type.desc().nullslast())
        .limit(1)
    )
    rule = result.scalar_one_or_none()

    if not rule:
        raise ValidationError(code="NO_PRICING_RULE", message="No active pricing rule found for this variant.")

    # Calculate price based on model
    unit_price, water_total = _calculate_water_price(rule, quantity_litres)

    # Delivery charge
    delivery_charge = await _calculate_delivery_charge(db, variant.delivery_method_id)

    # Tax
    tax_total = (water_total + delivery_charge) * TAX_RATE

    # Final
    final_total = water_total + delivery_charge + tax_total

    return QuoteResponse(
        variant_id=variant_id, quantity_litres=quantity_litres,
        unit_price=round(unit_price, 2), water_total=round(water_total, 2),
        delivery_charge=round(delivery_charge, 2), tax_total=round(tax_total, 2),
        final_total=round(final_total, 2),
        pricing_rule_id=rule.id, pricing_rule_version=rule.version,
    )


def _calculate_water_price(rule: PricingRule, quantity_litres: int) -> tuple[Decimal, Decimal]:
    """Calculate water price based on pricing model."""
    if rule.pricing_model == "FIXED":
        return rule.base_price, rule.base_price
    elif rule.pricing_model == "PER_LITRE":
        total = rule.base_price * quantity_litres
        return rule.base_price, total
    elif rule.pricing_model == "TIERED":
        if not rule.tiers:
            return rule.base_price, rule.base_price * quantity_litres
        for tier in sorted(rule.tiers, key=lambda t: t.get("min_litres", 0)):
            if tier.get("min_litres", 0) <= quantity_litres <= tier.get("max_litres", float("inf")):
                price = Decimal(str(tier["price_per_litre"]))
                return price, price * quantity_litres
        return rule.base_price, rule.base_price * quantity_litres
    return rule.base_price, rule.base_price * quantity_litres


async def _calculate_delivery_charge(db: AsyncSession, delivery_method_id: uuid.UUID) -> Decimal:
    result = await db.execute(
        select(DeliveryPricingRule)
        .where(DeliveryPricingRule.is_active == True)
        .where((DeliveryPricingRule.delivery_method_id == delivery_method_id) | (DeliveryPricingRule.delivery_method_id == None))
        .limit(1)
    )
    rule = result.scalar_one_or_none()
    if not rule:
        return Decimal("0")
    return rule.base_price


# ---- Admin CRUD ----

async def list_rules(db: AsyncSession) -> list[PricingRule]:
    result = await db.execute(select(PricingRule).order_by(PricingRule.created_at.desc()))
    return list(result.scalars().all())


async def create_rule(db: AsyncSession, data: PricingRuleCreate, actor_id: uuid.UUID) -> PricingRule:
    rule = PricingRule(**data.model_dump())
    db.add(rule)
    await db.flush()
    await audit_log(db, actor_id=actor_id, action="CREATE", entity_type="pricing_rule", entity_id=rule.id)
    return rule


async def update_rule(db: AsyncSession, rule_id: uuid.UUID, data: PricingRuleUpdate, actor_id: uuid.UUID) -> PricingRule:
    result = await db.execute(select(PricingRule).where(PricingRule.id == rule_id))
    rule = result.scalar_one_or_none()
    if not rule:
        raise NotFoundError("PricingRule", rule_id)
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(rule, field, value)
    rule.version += 1
    await db.flush()
    await audit_log(db, actor_id=actor_id, action="UPDATE", entity_type="pricing_rule", entity_id=rule_id)
    return rule
