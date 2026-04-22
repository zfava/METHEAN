#!/usr/bin/env bash
set -euo pipefail

# METHEAN Database Restore Script
# Usage: ./scripts/restore-db.sh <backup-file-name>
# Example: ./scripts/restore-db.sh methean_backup_20260422_020000.sql.gz

if [ -z "${1:-}" ]; then
  echo "Usage: $0 <backup-filename>"
  echo "List available backups:"
  echo "  aws s3 ls s3://${S3_BUCKET_NAME:-methean-artifacts}/backups/daily/ --endpoint-url ${S3_ENDPOINT_URL}"
  exit 1
fi

BACKUP_FILE="$1"
S3_BUCKET="${S3_BUCKET_NAME:-methean-artifacts}"
RESTORE_DIR="/tmp/restore"

mkdir -p "${RESTORE_DIR}"

echo "[$(date)] Downloading backup: ${BACKUP_FILE}"
aws s3 cp \
  "s3://${S3_BUCKET}/backups/daily/${BACKUP_FILE}" \
  "${RESTORE_DIR}/${BACKUP_FILE}" \
  --endpoint-url "${S3_ENDPOINT_URL}"

echo "[$(date)] Restoring database..."
gunzip -c "${RESTORE_DIR}/${BACKUP_FILE}" | \
  PGPASSWORD="${DB_PASSWORD}" psql \
    -h "${DB_HOST:-postgres}" \
    -p "${DB_PORT:-5432}" \
    -U "${DB_USER}" \
    -d "${DB_NAME}" \
    --single-transaction

rm -f "${RESTORE_DIR}/${BACKUP_FILE}"
echo "[$(date)] Restore complete."
