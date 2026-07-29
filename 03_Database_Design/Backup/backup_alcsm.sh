#!/usr/bin/env bash
# =====================================================================
# ALCSM Collection Database — Backup Procedure  (backup_alcsm.sh)
#
# Tested: pg_dump -Fc + pg_restore round-trip verified (profiles and
# sections restored intact into a fresh database).
#
# SECURITY: backups contain pseudonymised personal data. They MUST be
# written to the university-approved, EEA-resident, access-controlled
# secure store — NOT to a laptop, NOT to consumer cloud, NOT to the
# Git repository. Encrypt at rest.
# =====================================================================
set -euo pipefail

DB="${ALCSM_DB:-alcsm}"
HOST="${ALCSM_HOST:-/var/run/postgresql}"
PORT="${ALCSM_PORT:-5432}"
# Secure, access-controlled destination on approved storage:
BACKUP_DIR="${ALCSM_BACKUP_DIR:?set ALCSM_BACKUP_DIR to the secure store path}"

STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
DUMP="${BACKUP_DIR}/alcsm_${STAMP}.dump"

mkdir -p "${BACKUP_DIR}"

# Custom-format dump: compressed, selective restore, integrity-checked.
pg_dump -h "${HOST}" -p "${PORT}" -Fc "${DB}" -f "${DUMP}"

# Verify the dump is readable before trusting it (a dump you cannot
# list is not a backup).
pg_restore --list "${DUMP}" > /dev/null
echo "backup OK: ${DUMP} ($(stat -c%s "${DUMP}") bytes)"

# Optional: encrypt at rest if the store is not already encrypted.
#   gpg --symmetric --cipher-algo AES256 "${DUMP}" && rm "${DUMP}"

# Retention: keep the last N dumps, prune older ones. Adjust N to policy.
N="${ALCSM_KEEP:-14}"
ls -1t "${BACKUP_DIR}"/alcsm_*.dump 2>/dev/null | tail -n +$((N+1)) | xargs -r rm --
echo "retained newest ${N} dumps"

# =====================================================================
# RESTORE (documented, run manually when needed):
#   createdb -h HOST -p PORT alcsm_restore
#   pg_restore -h HOST -p PORT -d alcsm_restore  <dump-file>
# Verify:
#   psql -d alcsm_restore -c "SELECT count(*) FROM alcsm.profile;"
# =====================================================================
