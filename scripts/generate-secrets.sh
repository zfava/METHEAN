#!/bin/bash
# Generate cryptographically random secrets for METHEAN production deployment.
# Usage: ./scripts/generate-secrets.sh

set -euo pipefail

echo "# ══════════════ Generated Secrets ══════════════"
echo "# Generated at: $(date -u +"%Y-%m-%dT%H:%M:%SZ")"
echo "#"
echo "# ⚠️  Do not commit these values."
echo "# ⚠️  Add them to .env.prod only."
echo ""

JWT=$(openssl rand -base64 64 | tr -d '\n/+=')
echo "JWT_SECRET=${JWT:0:64}"
echo ""
echo "# Set to the OLD JWT_SECRET when rotating keys."
echo "# Leave empty on first deploy."
echo "PREVIOUS_JWT_SECRET="
echo ""

DB_PASS=$(openssl rand -base64 32 | tr -d '\n/+=')
echo "DB_PASSWORD=${DB_PASS:0:32}"
echo ""

echo "# ════════════════════════════════════════════════"
echo "# Copy the values above into your .env.prod file."
echo "# ════════════════════════════════════════════════"
