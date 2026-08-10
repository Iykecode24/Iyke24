# Troubleshooting Guide — Iyke Content Studio

## Common Issues

### Docker Services Won't Start

**Problem**: `docker compose up` fails or services crash on startup.

**Solutions**:
1. Check that Docker is running: `docker info`
2. Check port conflicts: `netstat -an | findstr "3000\|8000\|5432\|6379"`
3. View logs: `docker compose logs -f <service-name>`
4. Rebuild images: `docker compose build --no-cache`
5. Reset volumes: `docker compose down -v && docker compose up -d`

### Database Connection Errors

**Problem**: Backend shows "connection refused" to PostgreSQL.

**Solutions**:
1. Verify PostgreSQL is running: `docker compose ps postgres`
2. Check database URL in `.env` matches Docker Compose settings
3. Wait for PostgreSQL health check: `docker compose logs postgres`
4. Reset database: `docker compose down -v && docker compose up -d postgres`

### Migration Errors

**Problem**: `alembic upgrade head` fails.

**Solutions**:
1. Check that all model imports are in `app/models/__init__.py`
2. View migration history: `alembic history`
3. Reset migrations: `alembic downgrade base && alembic upgrade head`
4. Regenerate migrations: `alembic revision --autogenerate -m "reset"`

### Frontend Build Errors

**Problem**: Next.js fails to compile.

**Solutions**:
1. Clear cache: `rm -rf .next/ node_modules/ && npm install`
2. Check TypeScript errors: `npx tsc --noEmit`
3. Check environment variables are set in `.env.local`

### RunPod Connection Issues

**Problem**: RunPod API calls fail.

**Solutions**:
1. Verify API key in Admin Settings → Integrations
2. Test connection using the "Test" button
3. Check RunPod service status at https://status.runpod.io
4. Verify network volume is in the same datacenter as GPU
5. Check API key permissions

### GPU Instance Stuck Running

**Problem**: GPU instance won't stop or terminate.

**Solutions**:
1. Use Admin Settings → GPU Dashboard → Force Terminate
2. Log into RunPod console directly at https://runpod.io/console
3. Emergency shutdown: Set timer in Admin Settings → Cost Limits
4. Check for active jobs preventing shutdown

### Voice Generation Fails

**Problem**: ElevenLabs returns errors.

**Solutions**:
1. Check API key validity in Admin Settings
2. Verify usage quota hasn't been exceeded
3. Check voice ID is valid and accessible
4. Try reducing text length (API has limits per request)

### Media Upload Fails

**Problem**: File uploads return errors.

**Solutions**:
1. Check file size limits (default 50MB for images, 500MB for video)
2. Verify file type is allowed (JPEG, PNG, WebP, MP4, WAV)
3. Check storage credentials in Admin Settings
4. Verify storage bucket exists and has write permissions

## Getting Help

- Check API documentation: `/docs` endpoint
- Review error logs: `docker compose logs -f backend`
- Check audit logs: Admin Settings → Audit Logs
