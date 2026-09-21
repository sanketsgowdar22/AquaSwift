"""
AquaSwift — RBAC Schemas
"""

from __future__ import annotations

import uuid
from datetime import datetime

from pydantic import BaseModel


class RoleResponse(BaseModel):
    id: uuid.UUID
    name: str
    description: str | None
    permissions: list[str]
    created_at: datetime

    model_config = {"from_attributes": True}


class RoleListResponse(BaseModel):
    items: list[RoleResponse]


class AssignRoleRequest(BaseModel):
    role_name: str
