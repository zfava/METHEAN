#!/usr/bin/env bash
set -euo pipefail

# METHEAN Database Backup Script
# Runs daily via cron or container scheduler.
# Stores compressed backups in S3-compatible storage.
# Retains 30 days of daily backups and 12 months of monthly backups.

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
DAY_OF_MONTH=$(date +%d)
BACKUP_FILE="methean_backup_${TIMESTAMP}.sql.gz"
BACKUP_DIR="/tmp/backups"
S3_BUCKET="${S3_BUCKET_NAME:-methean-artifacts}"
S3_BACKUP_PREFIX="backups/daily"
S3_MONTHLY_PREFIX="backups/monthly"

mkdir -p "${BACKUP_DIR}"

echo "[$(date)] Starting database backup..."

# Create compressed backup
PGPASSWORD="${DB_PASSWORD}" pg_dump \
  -h "${DB_HOST:-postgres}" \
  -p "${DB_PORT:-5432}" \
  -U "${DB_USER}" \
  -d "${DB_NAME}" \
  --no-owner \
  --no-privileges \
  --verbose \
  2>/dev/null | gzip > "${BACKUP_DIR}/${BACKUP_FILE}"

BACKUP_SIZE=$(du -h "${BACKUP_DIR}/${BACKUP_FILE}" | cut -f1)
echo "[$(date)] Backup created: ${BACKUP_FILE} (${BACKUP_SIZE})"

# Upload to S3
aws s3 cp \
  "${BACKUP_DIR}/${BACKUP_FILE}" \
  "s3://${S3_BUCKET}/${S3_BACKUP_PREFIX}/${BACKUP_FILE}" \
  --endpoint-url "${S3_ENDPOINT_URL}" \
  2>/dev/null

echo "[$(date)] Uploaded to s3://${S3_BUCKET}/${S3_BACKUP_PREFIX}/${BACKUP_FILE}"

# On the 1st of the month, copy to monthly archive
if [ "${DAY_OF_MONTH}" = "01" ]; then
  MONTHLY_FILE="methean_monthly_$(date +%Y%m).sql.gz"
  aws s3 cp \
    "s3://${S3_BUCKET}/${S3_BACKUP_PREFIX}/${BACKUP_FILE}" \
    "s3://${S3_BUCKET}/${S3_MONTHLY_PREFIX}/${MONTHLY_FILE}" \
    --endpoint-url "${S3_ENDPOINT_URL}" \
    2>/dev/null
  echo "[$(date)] Monthly archive created: ${MONTHLY_FILE}"
fi

# Clean up daily backups older than 30 days
aws s3 ls "s3://${S3_BUCKET}/${S3_BACKUP_PREFIX}/" \
  --endpoint-url "${S3_ENDPOINT_URL}" 2>/dev/null | \
  while read -r line; do
    FILE_DATE=$(echo "${line}" | awk '{print $1}')
    FILE_NAME=$(echo "${line}" | awk '{print $4}')
    if [ -n "${FILE_NAME}" ]; then
      DAYS_OLD=$(( ( $(date +%s) - $(date -d "${FILE_DATE}" +%s 2>/dev/null || echo 0) ) / 86400 ))
      if [ "${DAYS_OLD}" -gt 30 ]; then
        aws s3 rm "s3://${S3_BUCKET}/${S3_BACKUP_PREFIX}/${FILE_NAME}" \
          --endpoint-url "${S3_ENDPOINT_URL}" 2>/dev/null
        echo "[$(date)] Pruned old backup: ${FILE_NAME} (${DAYS_OLD} days old)"
      fi
    fi
  done

# Clean up local temp
rm -f "${BACKUP_DIR}/${BACKUP_FILE}"

echo "[$(date)] Backup complete."
