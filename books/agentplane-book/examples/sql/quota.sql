-- SPDX-License-Identifier: MIT
-- Design fragment, not a standalone migration. Bind parameters in one transaction.
-- Keep one counter per scope; derive scope from authenticated identity.
BEGIN;
UPDATE quota_counters SET reserved = reserved + 1
WHERE organization_id = $1 AND project_id = $2
  AND reserved < capacity_limit
RETURNING reserved;
-- Require one updated row; then insert the uniquely scoped reservation record.
-- A duplicate reservation must roll back the increment, not commit it.
COMMIT;
