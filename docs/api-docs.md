# API Documentation — Iyke Content Studio

**Base URL**: `http://localhost:8000/api/v1`

**Authentication**: Bearer JWT token in `Authorization` header.

---

## Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/signup` | Create new account |
| POST | `/auth/login` | Login and receive JWT tokens |
| POST | `/auth/logout` | Invalidate session |
| POST | `/auth/refresh` | Refresh access token |
| POST | `/auth/password-reset/request` | Request password reset email |
| POST | `/auth/password-reset/confirm` | Reset password with token |
| POST | `/auth/mfa/setup` | Setup TOTP MFA |
| POST | `/auth/mfa/verify` | Verify MFA code |
| GET | `/auth/me` | Get current user profile |
| PUT | `/auth/me` | Update profile |

## Projects

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/projects` | List projects (paginated) |
| POST | `/projects` | Create project |
| GET | `/projects/{id}` | Get project details |
| PUT | `/projects/{id}` | Update project |
| DELETE | `/projects/{id}` | Delete project |
| POST | `/projects/{id}/duplicate` | Duplicate project |
| GET | `/projects/{id}/export` | Export project |

## Characters

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/characters` | List characters |
| POST | `/characters` | Create character |
| GET | `/characters/{id}` | Get character |
| PUT | `/characters/{id}` | Update character |
| DELETE | `/characters/{id}` | Delete character |
| POST | `/characters/{id}/upload-reference` | Upload reference image |
| POST | `/characters/{id}/save-to-library` | Save to library |

## Rendering

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/render/estimate-cost` | Estimate render cost |
| POST | `/render/start` | Start rendering |
| GET | `/render/jobs` | List render jobs |
| GET | `/render/jobs/{id}` | Get job status |
| POST | `/render/jobs/{id}/cancel` | Cancel job |
| POST | `/render/jobs/{id}/retry` | Retry failed job |
| GET | `/render/queue` | Get queue status |

## Media

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/media` | List media files |
| POST | `/media/upload` | Upload file |
| GET | `/media/{id}` | Get media details |
| DELETE | `/media/{id}` | Delete media |
| GET | `/media/{id}/signed-url` | Get signed download URL |

## Admin (requires admin role)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/admin/integrations` | List API integrations |
| POST | `/admin/integrations` | Add integration |
| PUT | `/admin/integrations/{id}` | Update integration |
| DELETE | `/admin/integrations/{id}` | Remove integration |
| POST | `/admin/integrations/{id}/test` | Test connection |
| GET | `/admin/models` | List registered models |
| GET | `/admin/gpu-instances` | List GPU instances |
| POST | `/admin/gpu-instances/{id}/stop` | Stop GPU |
| POST | `/admin/gpu-instances/{id}/terminate` | Terminate GPU |
| GET | `/admin/users` | List users |
| GET | `/admin/audit-logs` | View audit logs |
| GET | `/admin/stats` | System statistics |

## Real-time Events

| Protocol | Endpoint | Description |
|----------|----------|-------------|
| SSE | `/events/{project_id}` | Real-time render progress |

## Health

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Basic health check |
| GET | `/health/detailed` | Detailed system health (admin) |

---

Interactive API documentation is available at `/docs` (Swagger UI) and `/redoc` (ReDoc).
