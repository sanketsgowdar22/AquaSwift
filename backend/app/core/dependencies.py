"""
AquaSwift — FastAPI Dependencies

Reusable dependency factories for authorization and common parameters.
"""

from __future__ import annotations

from typing import Callable

from fastapi import Depends, HTTPException, status

from app.core.security import get_current_user


def require_permission(permission: str) -> Callable:
    """
    Factory that returns a FastAPI dependency enforcing a specific permission.

    Usage:
        @router.post("/admin/catalog")
        async def create(
            current_user = Depends(get_current_user),
            _ = Depends(require_permission("catalog:write")),
        ): ...

    The dependency loads the user's role permissions and checks if the
    required permission is granted. Raises 403 if not.
    """

    async def _check_permission(current_user=Depends(get_current_user)):
        # Lazy import to avoid circular dependency
        from app.rbac.service import check_user_permission

        has_permission = await check_user_permission(current_user, permission)
        if not has_permission:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "code": "INSUFFICIENT_PERMISSIONS",
                    "message": f"Permission '{permission}' is required.",
                },
            )
        return current_user

    return _check_permission
