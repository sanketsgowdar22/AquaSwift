"""
AquaSwift — Users Router
"""

from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.models import User
from app.core.database import get_db
from app.core.dependencies import require_permission
from app.core.security import get_current_user
from app.rbac.schemas import AssignRoleRequest
from app.users import service
from app.users.schemas import (
    AdminUpdateUserRequest,
    AdminUserListResponse,
    UpdateProfileRequest,
    UserProfileResponse,
)

router = APIRouter()


# ---- Customer-facing ----


@router.get("/users/me", response_model=UserProfileResponse, tags=["Users"])
async def get_my_profile(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get the authenticated user's profile."""
    profile = await service.get_user_profile(db, current_user)
    return profile


@router.patch("/users/me", response_model=UserProfileResponse, tags=["Users"])
async def update_my_profile(
    data: UpdateProfileRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Update the authenticated user's profile."""
    await service.update_profile(db, current_user, full_name=data.full_name)
    return await service.get_user_profile(db, current_user)


# ---- Admin ----


@router.get("/admin/users", response_model=AdminUserListResponse, tags=["Admin - Users"])
async def list_users(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    _=Depends(require_permission("customers:read")),
    db: AsyncSession = Depends(get_db),
):
    """List all users (admin)."""
    users, total = await service.list_users(db, page=page, page_size=page_size)
    total_pages = max(1, (total + page_size - 1) // page_size)
    return AdminUserListResponse(
        items=users,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
    )


@router.patch("/admin/users/{user_id}", tags=["Admin - Users"])
async def admin_update_user(
    user_id: uuid.UUID,
    data: AdminUpdateUserRequest,
    _=Depends(require_permission("customers:write")),
    db: AsyncSession = Depends(get_db),
):
    """Update a user's profile (admin)."""
    user = await service.admin_update_user(db, user_id, full_name=data.full_name, is_active=data.is_active)
    return await service.get_user_profile(db, user)


@router.post("/admin/users/{user_id}/roles", tags=["Admin - Users"])
async def assign_role(
    user_id: uuid.UUID,
    data: AssignRoleRequest,
    _=Depends(require_permission("roles:write")),
    db: AsyncSession = Depends(get_db),
):
    """Assign a role to a user (admin)."""
    await service.assign_role(db, user_id, data.role_name)
    return {"message": f"Role '{data.role_name}' assigned successfully."}
