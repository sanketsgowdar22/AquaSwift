"""002_config_and_business_tables

Create all remaining tables: catalog, addresses, sources, quality,
inventory, pricing, coupons, orders, vehicles, deliveries, payments,
notifications, reviews, B2B, and Phase 2/3 stubs.

Revision ID: 002
Revises: 001
Create Date: 2026-09-05
"""
from typing import Sequence, Union
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from alembic import op

revision: str = "002"
down_revision: Union[str, None] = "001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ---- Catalog ----
    op.create_table("water_purposes",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("name", sa.String(100), unique=True, nullable=False),
        sa.Column("description", sa.Text, nullable=True),
        sa.Column("icon_url", sa.String(500), nullable=True),
        sa.Column("display_order", sa.Integer, nullable=False, server_default="0"),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_table("water_quality_types",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("name", sa.String(100), unique=True, nullable=False),
        sa.Column("description", sa.Text, nullable=True),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_table("delivery_methods",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("name", sa.String(100), unique=True, nullable=False),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_table("water_purpose_qualities",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("purpose_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("water_purposes.id"), nullable=False),
        sa.Column("quality_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("water_quality_types.id"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.UniqueConstraint("purpose_id", "quality_id", name="uq_purpose_quality"),
    )
    op.create_table("water_variants",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("purpose_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("water_purposes.id"), nullable=False),
        sa.Column("quality_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("water_quality_types.id"), nullable=False),
        sa.Column("delivery_method_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("delivery_methods.id"), nullable=False),
        sa.Column("min_quantity_litres", sa.BigInteger, nullable=False),
        sa.Column("max_quantity_litres", sa.BigInteger, nullable=False),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.UniqueConstraint("purpose_id", "quality_id", "delivery_method_id", name="uq_variant_combo"),
        sa.CheckConstraint("min_quantity_litres > 0", name="ck_variant_min_qty"),
        sa.CheckConstraint("max_quantity_litres >= min_quantity_litres", name="ck_variant_max_gte_min"),
    )

    # ---- Sources ----
    op.create_table("water_sources",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("type", sa.String(50), nullable=False),
        sa.Column("gps_lat", sa.Numeric(10, 7), nullable=True),
        sa.Column("gps_lng", sa.Numeric(10, 7), nullable=True),
        sa.Column("capacity_litres", sa.BigInteger, nullable=False),
        sa.Column("status", sa.String(20), nullable=False, server_default="ACTIVE"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    # ---- Quality ----
    op.create_table("water_quality_records",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("source_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("water_sources.id"), nullable=False),
        sa.Column("ph_level", sa.Numeric(4, 2), nullable=True),
        sa.Column("tds", sa.Integer, nullable=True),
        sa.Column("turbidity", sa.Numeric(6, 2), nullable=True),
        sa.Column("treatment_type", sa.String(100), nullable=True),
        sa.Column("tested_by", sa.String(255), nullable=True),
        sa.Column("test_date", sa.Date, nullable=False),
        sa.Column("certificate_url", sa.String(500), nullable=True),
        sa.Column("status", sa.String(20), nullable=False, server_default="PENDING"),
        sa.Column("notes", sa.Text, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("idx_quality_records_source_id", "water_quality_records", ["source_id"])

    # ---- Addresses ----
    op.create_table("addresses",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("label", sa.String(50), nullable=True),
        sa.Column("address_line_1", sa.String(255), nullable=False),
        sa.Column("address_line_2", sa.String(255), nullable=True),
        sa.Column("city", sa.String(100), nullable=False),
        sa.Column("state", sa.String(100), nullable=False),
        sa.Column("pincode", sa.String(10), nullable=False),
        sa.Column("lat", sa.Numeric(10, 7), nullable=True),
        sa.Column("lng", sa.Numeric(10, 7), nullable=True),
        sa.Column("formatted_address", sa.Text, nullable=True),
        sa.Column("notes", sa.Text, nullable=True),
        sa.Column("is_default", sa.Boolean, nullable=False, server_default="false"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("idx_addresses_user_id", "addresses", ["user_id"])

    # ---- Inventory ----
    op.create_table("inventory_transactions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("source_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("water_sources.id"), nullable=False),
        sa.Column("type", sa.String(20), nullable=False),
        sa.Column("quantity_litres", sa.BigInteger, nullable=False),
        sa.Column("reference_type", sa.String(30), nullable=True),
        sa.Column("reference_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("notes", sa.Text, nullable=True),
        sa.Column("created_by", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("idx_inv_txn_source_id", "inventory_transactions", ["source_id"])
    op.create_index("idx_inv_txn_created_at", "inventory_transactions", ["created_at"])

    op.create_table("inventory_balances",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("source_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("water_sources.id"), unique=True, nullable=False),
        sa.Column("available_litres", sa.BigInteger, nullable=False, server_default="0"),
        sa.Column("reserved_litres", sa.BigInteger, nullable=False, server_default="0"),
        sa.Column("allocated_litres", sa.BigInteger, nullable=False, server_default="0"),
        sa.Column("last_reconciled_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    # ---- Pricing ----
    op.create_table("pricing_rules",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("version", sa.Integer, nullable=False, server_default="1"),
        sa.Column("purpose_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("water_purposes.id"), nullable=True),
        sa.Column("quality_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("water_quality_types.id"), nullable=True),
        sa.Column("customer_type", sa.String(20), nullable=True),
        sa.Column("area_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("pricing_model", sa.String(20), nullable=False),
        sa.Column("base_price", sa.Numeric(12, 2), nullable=False),
        sa.Column("tiers", postgresql.JSONB, nullable=True),
        sa.Column("active_from", sa.DateTime(timezone=True), nullable=False),
        sa.Column("active_to", sa.DateTime(timezone=True), nullable=True),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_table("delivery_pricing_rules",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("delivery_method_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("delivery_methods.id"), nullable=True),
        sa.Column("pricing_model", sa.String(20), nullable=False),
        sa.Column("base_price", sa.Numeric(12, 2), nullable=False),
        sa.Column("bands", postgresql.JSONB, nullable=True),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    # ---- Coupons ----
    op.create_table("coupons",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("code", sa.String(50), unique=True, nullable=False),
        sa.Column("discount_type", sa.String(20), nullable=False),
        sa.Column("discount_value", sa.Numeric(12, 2), nullable=False),
        sa.Column("min_order_amount", sa.Numeric(12, 2), nullable=True),
        sa.Column("max_discount_amount", sa.Numeric(12, 2), nullable=True),
        sa.Column("valid_from", sa.DateTime(timezone=True), nullable=False),
        sa.Column("valid_to", sa.DateTime(timezone=True), nullable=False),
        sa.Column("total_usage_limit", sa.Integer, nullable=True),
        sa.Column("per_customer_limit", sa.Integer, nullable=False, server_default="1"),
        sa.Column("current_usage_count", sa.Integer, nullable=False, server_default="0"),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    # ---- Orders ----
    op.create_table("orders",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("order_number", sa.String(20), unique=True, nullable=False),
        sa.Column("customer_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("address_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("addresses.id"), nullable=False),
        sa.Column("order_type", sa.String(20), nullable=False, server_default="STANDARD"),
        sa.Column("status", sa.String(30), nullable=False, server_default="PENDING_PAYMENT"),
        sa.Column("total_quantity_litres", sa.BigInteger, nullable=False),
        sa.Column("scheduled_window_start", sa.DateTime(timezone=True), nullable=True),
        sa.Column("scheduled_window_end", sa.DateTime(timezone=True), nullable=True),
        sa.Column("coupon_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("coupons.id"), nullable=True),
        sa.Column("idempotency_key", sa.String(64), unique=True, nullable=True),
        sa.Column("notes", sa.Text, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("idx_orders_customer_id", "orders", ["customer_id"])
    op.create_index("idx_orders_status", "orders", ["status"])

    op.create_table("order_items",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("order_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("orders.id"), nullable=False),
        sa.Column("variant_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("water_variants.id"), nullable=False),
        sa.Column("purpose_name", sa.String(100), nullable=False),
        sa.Column("quality_name", sa.String(100), nullable=False),
        sa.Column("delivery_method_name", sa.String(100), nullable=False),
        sa.Column("quantity_litres", sa.BigInteger, nullable=False),
        sa.Column("unit_price", sa.Numeric(12, 2), nullable=False),
        sa.Column("water_total", sa.Numeric(12, 2), nullable=False),
        sa.Column("delivery_charge", sa.Numeric(12, 2), nullable=False, server_default="0"),
        sa.Column("discount_total", sa.Numeric(12, 2), nullable=False, server_default="0"),
        sa.Column("tax_total", sa.Numeric(12, 2), nullable=False, server_default="0"),
        sa.Column("final_total", sa.Numeric(12, 2), nullable=False),
        sa.Column("pricing_rule_version_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("pricing_snapshot", postgresql.JSONB, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("idx_order_items_order_id", "order_items", ["order_id"])

    op.create_table("order_status_history",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("order_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("orders.id"), nullable=False),
        sa.Column("from_status", sa.String(30), nullable=False),
        sa.Column("to_status", sa.String(30), nullable=False),
        sa.Column("actor_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=True),
        sa.Column("reason", sa.Text, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    # ---- Vehicles ----
    op.create_table("vehicles",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("registration_number", sa.String(20), unique=True, nullable=False),
        sa.Column("type", sa.String(50), nullable=False),
        sa.Column("capacity_litres", sa.BigInteger, nullable=False),
        sa.Column("status", sa.String(20), nullable=False, server_default="ACTIVE"),
        sa.Column("current_driver_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("driver_profiles.id"), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    # ---- Deliveries ----
    op.create_table("deliveries",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("order_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("orders.id"), nullable=False),
        sa.Column("source_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("water_sources.id"), nullable=True),
        sa.Column("driver_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("driver_profiles.id"), nullable=True),
        sa.Column("vehicle_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("vehicles.id"), nullable=True),
        sa.Column("status", sa.String(25), nullable=False, server_default="PENDING_ASSIGNMENT"),
        sa.Column("quantity_litres", sa.BigInteger, nullable=False),
        sa.Column("delivered_quantity_litres", sa.BigInteger, nullable=True),
        sa.Column("otp_code", sa.String(6), nullable=True),
        sa.Column("proof_photo_url", sa.String(500), nullable=True),
        sa.Column("gps_lat", sa.Numeric(10, 7), nullable=True),
        sa.Column("gps_lng", sa.Numeric(10, 7), nullable=True),
        sa.Column("parent_delivery_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("deliveries.id"), nullable=True),
        sa.Column("scheduled_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("idx_deliveries_order_id", "deliveries", ["order_id"])
    op.create_index("idx_deliveries_driver_id", "deliveries", ["driver_id"])
    op.create_index("idx_deliveries_status", "deliveries", ["status"])

    op.create_table("delivery_assignments",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("delivery_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("deliveries.id"), nullable=False),
        sa.Column("driver_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("driver_profiles.id"), nullable=False),
        sa.Column("status", sa.String(20), nullable=False),
        sa.Column("offered_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("responded_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("rejection_reason", sa.Text, nullable=True),
        sa.Column("attempt_number", sa.Integer, nullable=False),
    )

    op.create_table("delivery_events",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("delivery_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("deliveries.id"), nullable=False),
        sa.Column("event_type", sa.String(30), nullable=False),
        sa.Column("actor_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=True),
        sa.Column("metadata", postgresql.JSONB, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    # ---- Payments ----
    op.create_table("payments",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("order_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("orders.id"), nullable=False),
        sa.Column("amount", sa.Numeric(12, 2), nullable=False),
        sa.Column("currency", sa.String(3), nullable=False, server_default="INR"),
        sa.Column("status", sa.String(20), nullable=False, server_default="INITIATED"),
        sa.Column("gateway", sa.String(30), nullable=False, server_default="razorpay"),
        sa.Column("gateway_order_id", sa.String(100), nullable=True),
        sa.Column("gateway_payment_id", sa.String(100), nullable=True),
        sa.Column("idempotency_key", sa.String(64), unique=True, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("idx_payments_order_id", "payments", ["order_id"])

    op.create_table("payment_transactions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("payment_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("payments.id"), nullable=False),
        sa.Column("gateway_reference_id", sa.String(100), nullable=True),
        sa.Column("event_type", sa.String(50), nullable=False),
        sa.Column("raw_payload", postgresql.JSONB, nullable=False),
        sa.Column("verified_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    op.create_table("refunds",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("payment_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("payments.id"), nullable=False),
        sa.Column("amount", sa.Numeric(12, 2), nullable=False),
        sa.Column("reason", sa.Text, nullable=False),
        sa.Column("status", sa.String(20), nullable=False, server_default="INITIATED"),
        sa.Column("gateway_refund_id", sa.String(100), nullable=True),
        sa.Column("initiated_by", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    # ---- Notifications ----
    op.create_table("notifications",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("body", sa.Text, nullable=False),
        sa.Column("channel", sa.String(20), nullable=False, server_default="push"),
        sa.Column("event_type", sa.String(50), nullable=True),
        sa.Column("reference_type", sa.String(30), nullable=True),
        sa.Column("reference_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("is_read", sa.Boolean, nullable=False, server_default="false"),
        sa.Column("metadata", postgresql.JSONB, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("idx_notifications_user_id", "notifications", ["user_id"])

    op.create_table("device_tokens",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("token", sa.String(500), nullable=False),
        sa.Column("platform", sa.String(20), nullable=False),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    # ---- Reviews ----
    op.create_table("reviews",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("order_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("orders.id"), nullable=False),
        sa.Column("customer_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("driver_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("driver_profiles.id"), nullable=True),
        sa.Column("rating", sa.Integer, nullable=False),
        sa.Column("comment", sa.Text, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.UniqueConstraint("order_id", "customer_id", name="uq_review_order_customer"),
    )

    # ---- B2B ----
    op.create_table("businesses",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("registration_number", sa.String(100), nullable=True),
        sa.Column("contact_email", sa.String(255), nullable=True),
        sa.Column("contact_phone", sa.String(15), nullable=True),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_table("business_users",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("business_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("businesses.id"), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("role", sa.String(20), nullable=False),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.UniqueConstraint("business_id", "user_id", name="uq_business_user"),
    )
    op.create_table("business_sites",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("business_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("businesses.id"), nullable=False),
        sa.Column("address_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("addresses.id"), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("contact_person", sa.String(255), nullable=True),
        sa.Column("contact_phone", sa.String(15), nullable=True),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_table("bulk_requests",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("business_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("businesses.id"), nullable=False),
        sa.Column("site_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("business_sites.id"), nullable=True),
        sa.Column("purpose_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("water_purposes.id"), nullable=False),
        sa.Column("quality_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("water_quality_types.id"), nullable=False),
        sa.Column("total_quantity_litres", sa.BigInteger, nullable=False),
        sa.Column("frequency", sa.String(20), nullable=True),
        sa.Column("schedule_start", sa.Date, nullable=False),
        sa.Column("schedule_end", sa.Date, nullable=True),
        sa.Column("status", sa.String(20), nullable=False, server_default="PENDING"),
        sa.Column("notes", sa.Text, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_table("bulk_quotes",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("bulk_request_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("bulk_requests.id"), nullable=False),
        sa.Column("price_per_litre", sa.Numeric(12, 4), nullable=False),
        sa.Column("total_price", sa.Numeric(12, 2), nullable=False),
        sa.Column("delivery_charge", sa.Numeric(12, 2), nullable=False, server_default="0"),
        sa.Column("valid_until", sa.DateTime(timezone=True), nullable=False),
        sa.Column("status", sa.String(20), nullable=False, server_default="PENDING"),
        sa.Column("created_by", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    # ---- Phase 2/3 Stubs ----
    op.create_table("recurring_orders",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("customer_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("variant_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("water_variants.id"), nullable=False),
        sa.Column("address_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("addresses.id"), nullable=False),
        sa.Column("quantity_litres", sa.BigInteger, nullable=False),
        sa.Column("frequency", sa.String(20), nullable=False),
        sa.Column("schedule_days", postgresql.JSONB, nullable=True),
        sa.Column("preferred_window_start", sa.Time, nullable=True),
        sa.Column("preferred_window_end", sa.Time, nullable=True),
        sa.Column("status", sa.String(20), nullable=False, server_default="ACTIVE"),
        sa.Column("next_instance_date", sa.Date, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_table("recurring_order_instances",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("recurring_order_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("recurring_orders.id"), nullable=False),
        sa.Column("order_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("orders.id"), nullable=True),
        sa.Column("scheduled_date", sa.Date, nullable=False),
        sa.Column("status", sa.String(20), nullable=False, server_default="PENDING"),
        sa.Column("failure_reason", sa.Text, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_table("invoices",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("invoice_number", sa.String(30), unique=True, nullable=False),
        sa.Column("business_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("businesses.id"), nullable=False),
        sa.Column("billing_period_start", sa.Date, nullable=False),
        sa.Column("billing_period_end", sa.Date, nullable=False),
        sa.Column("subtotal", sa.Numeric(12, 2), nullable=False),
        sa.Column("tax_total", sa.Numeric(12, 2), nullable=False, server_default="0"),
        sa.Column("total", sa.Numeric(12, 2), nullable=False),
        sa.Column("status", sa.String(20), nullable=False, server_default="PENDING"),
        sa.Column("due_date", sa.Date, nullable=False),
        sa.Column("payment_terms_days", sa.Integer, nullable=False, server_default="30"),
        sa.Column("pdf_url", sa.String(500), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )


def downgrade() -> None:
    tables = [
        "invoices", "recurring_order_instances", "recurring_orders",
        "bulk_quotes", "bulk_requests", "business_sites", "business_users", "businesses",
        "reviews", "device_tokens", "notifications",
        "refunds", "payment_transactions", "payments",
        "delivery_events", "delivery_assignments", "deliveries", "vehicles",
        "order_status_history", "order_items", "orders",
        "coupons", "delivery_pricing_rules", "pricing_rules",
        "inventory_balances", "inventory_transactions",
        "addresses", "water_quality_records", "water_sources",
        "water_variants", "water_purpose_qualities", "delivery_methods",
        "water_quality_types", "water_purposes",
    ]
    for t in tables:
        op.drop_table(t)
