# WoW — Role-Based Access Control (RBAC)

## 1. Overview

WoW uses a role-based access control model where:

- Users are assigned **roles**
- Roles contain **permissions**
- API endpoints are protected by **permission checks**
- Authorization is enforced **server-side** (backend)

## 2. Role Model

| Role | Description | Target Users |
|------|------------|-------------|
| `CUSTOMER` | Default role for customers | App users (OTP login) |
| `DRIVER` | Delivery drivers | Driver portal users |
| `ADMIN` | Operations staff | Dashboard users |
| `SUPER_ADMIN` | Full system access | Platform owners |

### Role Hierarchy

```
SUPER_ADMIN → has all permissions
ADMIN       → has admin-level permissions
DRIVER      → has driver-specific permissions
CUSTOMER    → has customer-specific permissions
```

## 3. Permission Categories

| Category | Permissions | Used By |
|----------|-----------|---------|
| `customers` | `customers:read`, `customers:write` | ADMIN, SUPER_ADMIN |
| `drivers` | `drivers:read`, `drivers:write` | ADMIN, SUPER_ADMIN |
| `orders` | `orders:read`, `orders:cancel` | ADMIN, SUPER_ADMIN |
| `deliveries` | `deliveries:read`, `deliveries:assign` | ADMIN, SUPER_ADMIN |
| `catalog` | `catalog:read`, `catalog:write` | ADMIN, SUPER_ADMIN |
| `inventory` | `inventory:read`, `inventory:adjust` | ADMIN, SUPER_ADMIN |
| `pricing` | `pricing:read`, `pricing:write` | ADMIN, SUPER_ADMIN |
| `coupons` | `coupons:read`, `coupons:write` | ADMIN, SUPER_ADMIN |
| `payments` | `payments:read` | ADMIN, SUPER_ADMIN |
| `refunds` | `refunds:read`, `refunds:write` | ADMIN, SUPER_ADMIN |
| `reports` | `reports:read` | ADMIN, SUPER_ADMIN |
| `audit` | `audit:read` | SUPER_ADMIN |
| `roles` | `roles:read`, `roles:write` | SUPER_ADMIN |
| `vehicles` | `vehicles:read`, `vehicles:write` | ADMIN, SUPER_ADMIN |
| `sources` | `sources:read`, `sources:write` | ADMIN, SUPER_ADMIN |
| `businesses` | `businesses:read`, `businesses:write` | ADMIN, SUPER_ADMIN |
| `dashboard` | `dashboard:read` | ADMIN, SUPER_ADMIN |

## 4. Endpoint Protection Pattern

### Backend Implementation

```python
# In router.py
from app.core.dependencies import require_permission

@router.get("/admin/orders")
async def list_orders(
    user=Depends(require_permission("orders:read")),
    db=Depends(get_db),
):
    ...
```

### Customer Endpoints

Customer endpoints use `get_current_user()` dependency — no role check needed since authenticated = authorized for own resources. Resource ownership is enforced by filtering queries to the current user's ID.

### Driver Endpoints

Driver endpoints use `get_current_user()` + verify `DRIVER` role. Drivers can only access their own deliveries/profile.

### Admin Endpoints

Admin endpoints use `require_permission()` with specific permission strings. All `/admin/*` routes require authentication + admin role + specific permission.

## 5. Implementation Files

| File | Purpose |
|------|---------|
| `backend/app/rbac/models.py` | Role, Permission, UserRole models |
| `backend/app/rbac/schemas.py` | Role/Permission request/response schemas |
| `backend/app/rbac/service.py` | Role assignment, permission checking |
| `backend/app/rbac/router.py` | Admin role management endpoints |
| `backend/app/core/dependencies.py` | `get_current_user()`, `require_permission()` |

## 6. Frontend RBAC

The frontend provides **client-side hints** only. Actual authorization is enforced server-side.

```typescript
// frontend/lib/auth.tsx
const hasRole = (role: string) => user?.roles?.includes(role) ?? false;
const hasPermission = (permission: string) => {
  if (hasRole("SUPER_ADMIN")) return true;
  return false; // V1: role-based only, server enforces
};
```

## 7. Testing Requirements (Phase 1)

- Verify unauthenticated requests return 401
- Verify wrong-role requests return 403
- Verify correct-role requests succeed
- Verify SUPER_ADMIN bypasses all permission checks
- Verify customer can only access own resources
- Verify driver can only access own deliveries
