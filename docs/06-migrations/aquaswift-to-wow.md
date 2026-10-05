# AquaSwift → WoW Migration

## 1. Overview

The project was renamed from **AquaSwift** to **WoW (Water on Way)** as part of a complete rebrand. This document tracks all naming references and their migration status.

## 2. Migration Status

### Completed ✅

| Area | Before | After | Status |
|------|--------|-------|--------|
| Backend config default | `APP_NAME: str = "AquaSwift"` | `APP_NAME: str = "WoW"` | ✅ Done |
| Backend `.env` | `APP_NAME=AquaSwift` | `APP_NAME=WoW` | ✅ Done |
| Backend `.env.example` | `APP_NAME=AquaSwift` | `APP_NAME=WoW` | ✅ Done |
| Backend `.env` DB URL | `aquaswift:aquaswift_dev` | `wow:wow_dev` | ✅ Done |
| Backend `.env` email | `noreply@aquaswift.in` | `noreply@wow.in` | ✅ Done |
| Backend `.env` S3 bucket | `aquaswift-media-dev` | `wow-media-dev` | ✅ Done |
| Backend `.env` SMS sender | `AQUASW` | `WOWWTD` | ✅ Done |
| Backend docstrings | `AquaSwift —` | `WoW —` | ✅ Done |
| Docker container names | `aquaswift-*` | `wow-*` | ✅ Done |
| Docker DB credentials | `aquaswift` | `wow` | ✅ Done |
| Frontend page titles | `AquaSwift` | `WoW` | ✅ Done |
| Frontend components | `AquaswiftLogo` | `WowLogo` | ✅ Done |
| Frontend auth context | Various `aquaswift` refs | `wow` refs | ✅ Done |
| README.md | `AquaSwift` | `WoW` | ✅ Done |
| Swagger/OpenAPI title | `AquaSwift` | `WoW` | ✅ Done |

### Remaining ⚠️

| Area | File | Reference | Classification | Action |
|------|------|-----------|---------------|--------|
| Frontend `.env.example` | `frontend/.env.example` line 1 | `# AquaSwift Frontend Environment Variables` | Comment — safe to change | **Fix in P0** |
| Backend config SMS sender | `backend/app/core/config.py` line 66 | `MSG91_SENDER_ID: str = "AQUASW"` | Default value, overridden by .env | **Fix in P0** |
| Order number prefix | `docs/02-modules/orders/TASKS.md` T-ORD-011 | `AQ-{YYYYMMDD}-{sequential}` | Documentation reference | **Update to `WOW-` prefix** |

### Not Changed (Intentional)

| Area | Reference | Reason |
|------|-----------|--------|
| Repository directory name | `d:\Aquaswift\` | Filesystem path — would break git history; rename only when migrating to new hosting |
| Git remote URL | `sanketsgowdar22/AquaSwift` | GitHub repository name — rename separately via GitHub settings |
| Historical git commits | Various `AquaSwift` references | Commit history is immutable |

## 3. Remaining Actions

### P0 Actions (Documentation Phase)

1. Fix `frontend/.env.example` line 1 comment
2. Fix `backend/app/core/config.py` MSG91_SENDER_ID default
3. Update T-ORD-011 order number prefix from `AQ-` to `WOW-`

### Future Considerations

- Rename GitHub repository from `AquaSwift` to `WoW` when ready
- Update any CI/CD pipeline references
- Update any deployment scripts
- Update any external service configurations (MSG91, Razorpay, etc.)
