"""AquaSwift — Pricing Router"""
from __future__ import annotations
import uuid
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.auth.models import User
from app.core.database import get_db
from app.core.dependencies import require_permission
from app.core.security import get_current_user
from app.pricing import service
from app.pricing.schemas import PricingRuleCreate, PricingRuleResponse, PricingRuleUpdate, QuoteRequest, QuoteResponse

router = APIRouter()


@router.post("/pricing/quote", response_model=QuoteResponse, tags=["Pricing"])
async def get_quote(data: QuoteRequest, db: AsyncSession = Depends(get_db)):
    """Get a price quote for a variant and quantity. Public endpoint."""
    return await service.quote(db, data.variant_id, data.quantity_litres, data.customer_type)


@router.get("/admin/pricing/rules", response_model=list[PricingRuleResponse], tags=["Admin - Pricing"])
async def list_rules(_=Depends(require_permission("pricing:read")), db: AsyncSession = Depends(get_db)):
    return await service.list_rules(db)


@router.post("/admin/pricing/rules", response_model=PricingRuleResponse, tags=["Admin - Pricing"])
async def create_rule(data: PricingRuleCreate, user: User = Depends(require_permission("pricing:write")),
                      db: AsyncSession = Depends(get_db)):
    return await service.create_rule(db, data, user.id)


@router.patch("/admin/pricing/rules/{rule_id}", response_model=PricingRuleResponse, tags=["Admin - Pricing"])
async def update_rule(rule_id: uuid.UUID, data: PricingRuleUpdate,
                      user: User = Depends(require_permission("pricing:write")),
                      db: AsyncSession = Depends(get_db)):
    return await service.update_rule(db, rule_id, data, user.id)
