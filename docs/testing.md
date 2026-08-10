# Testing Guide — Iyke Content Studio

## Test Setup

### Backend Tests
```bash
cd backend
pip install pytest pytest-asyncio pytest-cov httpx

# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ -v --cov=app --cov-report=html

# Run specific test file
pytest tests/unit/test_auth.py -v

# Run specific test
pytest tests/unit/test_auth.py::test_password_hashing -v
```

### Frontend Tests
```bash
cd frontend
npm install -D @testing-library/react @testing-library/jest-dom jest

# Run all tests
npm test

# Run with coverage
npm test -- --coverage
```

## Test Categories

### Unit Tests
| File | Covers |
|------|--------|
| `test_auth.py` | Password hashing, JWT tokens, MFA |
| `test_encryption.py` | API key encryption/decryption, masking |
| `test_content_filter.py` | Text safety checks, consent requirements |
| `test_cost_service.py` | Cost estimation, limit checks |
| `test_file_scanner.py` | MIME validation, size limits, metadata stripping |
| `test_model_router.py` | Task routing, availability checks |

### Integration Tests
| File | Covers |
|------|--------|
| `test_auth_api.py` | Signup, login, password reset, MFA flows |
| `test_projects_api.py` | CRUD operations, permissions |
| `test_admin_api.py` | Integration management, user management |
| `test_render_api.py` | Job creation, status tracking |

### Security Tests
| Test | Verifies |
|------|----------|
| Rate limiting | Requests blocked after limit |
| RBAC | Unauthorized role denied |
| JWT expiration | Expired tokens rejected |
| Input validation | Malicious input sanitized |
| File upload | Invalid MIME types rejected |
| SQL injection | Parameterized queries safe |
| Secret masking | API keys not exposed |

### GPU Lifecycle Tests
Critical workflow that must be tested end-to-end:

1. ✅ Start RunPod Pod with correct GPU type
2. ✅ Attach network volume
3. ✅ Verify model is loaded
4. ✅ Submit render job
5. ✅ Monitor progress updates
6. ✅ Upload result to cloud storage
7. ✅ Confirm upload integrity
8. ✅ Stop/Terminate Pod
9. ✅ Verify Pod is terminated via API
10. ✅ Confirm billing has stopped
11. ✅ Record final cost

### Failure Recovery Tests
| Scenario | Expected Behavior |
|----------|-------------------|
| GPU crashes mid-render | Job marked failed, GPU terminated, retry queued |
| Upload fails | Retry upload, keep GPU alive until confirmed |
| API key invalid | Clear error message, job not started |
| Cost limit exceeded | Render blocked with explanation |
| Duplicate job submission | Prevented, existing job returned |
| Worker timeout | Emergency shutdown triggered |

## Running Tests in Docker

```bash
# Backend tests
docker compose exec backend pytest tests/ -v --tb=short

# All tests with coverage report
docker compose exec backend pytest tests/ --cov=app --cov-report=term-missing
```

## Continuous Integration

Tests should run on every pull request:
- Unit tests (fast, no external deps)
- Integration tests (requires test database)
- Lint checks (ruff, mypy)
- Frontend build verification
- Security scan (dependency audit)
