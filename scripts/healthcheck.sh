#!/bin/bash
# METHEAN production health check — verifies all services are running.
# Usage: ./scripts/healthcheck.sh [--host HOST]

set -euo pipefail

HOST="${1:-localhost}"
if [ "$1" = "--host" ] 2>/dev/null; then HOST="${2:-localhost}"; fi

PASS=0
FAIL=0
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

check() {
    local name="$1"
    local cmd="$2"
    if eval "$cmd" > /dev/null 2>&1; then
        echo "  ✓ ${name} — OK"
        PASS=$((PASS + 1))
    else
        echo "  ✗ ${name} — FAILED"
        FAIL=$((FAIL + 1))
    fi
}

echo "METHEAN Health Check — ${TIMESTAMP}"
echo "Host: ${HOST}"
echo ""

check "Backend API" "curl -sf http://${HOST}:8000/health"
check "Backend Ready" "curl -sf http://${HOST}:8000/health/ready"
check "PostgreSQL" "pg_isready -h ${HOST} -p 5432 -q 2>/dev/null || docker compose exec -T postgres pg_isready -q"
check "Redis" "redis-cli -h ${HOST} ping 2>/dev/null || docker compose exec -T redis redis-cli ping"

echo ""
echo "Results: ${PASS} passed, ${FAIL} failed"

if [ "$FAIL" -gt 0 ]; then
    echo "STATUS: UNHEALTHY"
    exit 1
else
    echo "STATUS: HEALTHY"
    exit 0
fi
