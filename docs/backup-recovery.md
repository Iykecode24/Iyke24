# Backup & Recovery Guide — Iyke Content Studio

## What to Back Up

| Component | Location | Backup Method | Frequency |
|-----------|----------|--------------|-----------|
| PostgreSQL Database | Docker volume / Managed DB | pg_dump | Daily |
| Media Files | Cloud Storage (R2/S3) | Cross-region replication | Continuous |
| Environment Config | `.env` file | Encrypted file backup | On change |
| RunPod Network Volume | RunPod storage | Manual snapshot | Weekly |
| Application Code | Git repository | Git push | On deploy |

## Database Backup

### Manual Backup
```bash
# From Docker
docker compose exec postgres pg_dump -U iyke -Fc iyke_studio > backup_$(date +%Y%m%d_%H%M%S).dump

# From managed database
pg_dump -h <host> -U <user> -Fc iyke_studio > backup.dump
```

### Automated Backup (cron)
```bash
# Add to crontab: daily backup at 2 AM
0 2 * * * docker compose -f /path/to/docker-compose.yml exec -T postgres pg_dump -U iyke -Fc iyke_studio > /backups/db_$(date +\%Y\%m\%d).dump
```

### Restore Database
```bash
# Restore from custom format dump
docker compose exec -T postgres pg_restore -U iyke -d iyke_studio --clean < backup.dump

# Restore from SQL dump
cat backup.sql | docker compose exec -T postgres psql -U iyke -d iyke_studio
```

## Media File Backup

Media files are stored in cloud storage (R2/S3). Configure backup at the provider level:

### Cloudflare R2
- Enable versioning on the bucket
- Use lifecycle rules for automatic deletion of old versions

### AWS S3
- Enable versioning
- Configure cross-region replication
- Set up lifecycle policies

## Environment Configuration
```bash
# Encrypt and backup .env
gpg -c .env  # Creates .env.gpg
# Store .env.gpg in a secure location (not in the code repository)
```

## Disaster Recovery Procedure

1. **Provision new infrastructure** (Docker host / cloud)
2. **Restore environment**: Decrypt `.env.gpg` → `.env`
3. **Start services**: `docker compose up -d postgres redis`
4. **Restore database**: `pg_restore` from latest backup
5. **Start application**: `docker compose up -d`
6. **Verify**: Check `/api/v1/health/detailed`
7. **Verify media**: Confirm cloud storage connectivity
8. **Test**: Create a test project to verify full functionality
