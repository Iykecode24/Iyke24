# Deployment Guide — Iyke Content Studio

## Architecture Overview

Iyke Content Studio runs as a distributed system:

| Component | Deployment Target | Purpose |
|-----------|------------------|---------|
| Frontend (Next.js) | Vercel / VPS / Docker | User interface |
| Backend (FastAPI) | VPS / Docker / Cloud Run | API, orchestration |
| Celery Workers | VPS / Docker | Background job processing |
| PostgreSQL | Managed DB / Docker | Data storage |
| Redis | Managed Redis / Docker | Cache, queue, pub/sub |
| GPU Workers | RunPod | AI model rendering |
| Storage | Cloudflare R2 / S3 | Media file storage |

## Docker Deployment

### Prerequisites
- Docker Engine 24+
- Docker Compose v2
- Minimum 4GB RAM, 20GB disk

### Steps

1. Clone the repository and create `.env`:
   ```bash
   cp .env.example .env
   # Edit .env with production values
   ```

2. Build and start:
   ```bash
   docker compose -f docker-compose.prod.yml up -d --build
   ```

3. Run migrations:
   ```bash
   docker compose exec backend alembic upgrade head
   ```

4. Create admin user:
   ```bash
   docker compose exec backend python -m app.scripts.create_admin
   ```

## Environment Configuration

See `.env.example` for all required variables.

### Critical Security Settings for Production
- Set `APP_ENV=production`
- Set `APP_DEBUG=false`
- Generate strong random values for `APP_SECRET_KEY` and `JWT_SECRET_KEY`
- Generate `ENCRYPTION_KEY` with: `python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"`
- Configure CORS_ORIGINS to your frontend domain only
- Enable HTTPS with proper SSL certificates

## Backup & Recovery

### Database Backup
```bash
docker compose exec postgres pg_dump -U iyke iyke_studio > backup_$(date +%Y%m%d).sql
```

### Database Restore
```bash
cat backup.sql | docker compose exec -T postgres psql -U iyke iyke_studio
```

### Media Files
Media files are stored in cloud storage (R2/S3) and should have their own backup policy configured at the storage provider level.

## Monitoring

- API health check: `GET /api/v1/health`
- Detailed health: `GET /api/v1/health/detailed` (admin auth required)
- GPU dashboard: Admin Settings → GPU Management
- Cost tracking: Admin Settings → Usage & Costs

## Scaling

- **Horizontal scaling**: Run multiple backend instances behind a load balancer
- **Worker scaling**: Increase Celery worker concurrency or add more worker containers
- **GPU scaling**: Configure max simultaneous GPU instances in Admin Settings
- **Database**: Move to managed PostgreSQL (AWS RDS, Cloud SQL, etc.)
- **Redis**: Move to managed Redis (ElastiCache, Upstash, etc.)
