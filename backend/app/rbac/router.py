"""
AquaSwift — RBAC Router
"""

from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import require_permission
from app.rbac import service
from app.rbac.schemas import RoleListResponse, RoleResponse

router = APIRouter()


@router.get("/admin/roles", response_model=RoleListResponse, tags=["RBAC"])
async def list_roles(
    _=Depends(require_permission("roles:read")),
    db: AsyncSession = Depends(get_db),
):
    """List all platform roles with their permissions."""
    roles = await service.get_all_roles(db)
    return RoleListResponse(items=[RoleResponse.model_validate(r) for r in roles])
