-- SPDX-License-Identifier: MIT
-- $1 job, $2 attempt, $3 fence, $4 authenticated runner, $5 outcome.
-- Simplified active-attempt completion only. A cancellation handshake needs
-- its own transition; an uncertain attempt needs reconciliation.
-- An empty result is not permission to force a state change.
PREPARE complete_job(text, text, bigint, text, text) AS
WITH completed AS (
    UPDATE jobs
    SET state = $5
    WHERE id = $1 AND current_attempt_id = $2 AND fence = $3
      AND lease_runner = $4 AND lease_until > statement_timestamp()
      AND state IN ('leased', 'running')
      AND $5 IN ('succeeded', 'failed')
    RETURNING id, current_attempt_id
)
UPDATE attempts AS a
SET state = $5, finished_at = statement_timestamp()
FROM completed AS j
WHERE a.id = j.current_attempt_id AND a.job_id = j.id
RETURNING a.id, a.job_id, a.state;
