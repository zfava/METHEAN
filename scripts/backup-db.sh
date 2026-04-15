#!/bin/bash
# METHEAN database backup script.
# Usage: ./scripts/backup-db.sh
# Reads DB credentials from .env.prod or environment variables.

set -euo pipefail

# Load env if available
if [ -f .env.prod ]; then
    set -a; source .env.prod; set +a
fi

DB_USER="${DB_USER:-methean_prod}"
DB_PASSWORD="${DB_PASSWORD:-}"
DB_NAME="${DB_NAME:-methean_prod}"
DB_HOST="${DB_HOST:-postgres}"
BACKUP_DIR="./backups"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="${BACKUP_DIR}/methean_${DATE}.sql.gz"
RETENTION_DAYS=30

# Create backup directory
mkdir -p "${BACKUP_DIR}"

echo "Starting backup: ${DB_NAME}@${DB_HOST}"

# Dump and compress
if PGPASSWORD="${DB_PASSWORD}" pg_dump -h "${DB_HOST}" -U "${DB_USER}" "${DB_NAME}" | gzip > "${BACKUP_FILE}"; then
    SIZE=$(du -h "${BACKUP_FILE}" | cut -f1)
    echo "  ✓ Backup created: ${BACKUP_FILE} (${SIZE})"
else
    echo "  ✗ Backup FAILED"
    rm -f "${BACKUP_FILE}"
    exit 1
fi

# Clean old backups
DELETED=$(find "${BACKUP_DIR}" -name "methean_*.sql.gz" -mtime +${RETENTION_DAYS} -delete -print | wc -l)
REMAINING=$(find "${BACKUP_DIR}" -name "methean_*.sql.gz" | wc -l)

echo "  Deleted ${DELETED} backups older than ${RETENTION_DAYS} days"
echo "  ${REMAINING} backups remaining"
