-- SPDX-License-Identifier: MIT
-- Teaching schema for a disposable database. Not a production migration.
-- Capacity, authorization, dependencies, cancellation, logs and outbox omitted.
CREATE TABLE jobs (
    id text PRIMARY KEY,
    project_id text NOT NULL,
    pool_id text NOT NULL,
    state text NOT NULL DEFAULT 'queued'
        CHECK (state IN ('queued','leased','running','cancel_requested',
                         'uncertain','succeeded','failed','cancelled')),
    priority integer NOT NULL DEFAULT 0,
    ready_at timestamptz NOT NULL DEFAULT statement_timestamp(),
    fence bigint NOT NULL DEFAULT 0 CHECK (fence >= 0),
    current_attempt_id text,
    lease_runner text,
    lease_until timestamptz,
    CHECK ((current_attempt_id IS NULL) = (lease_runner IS NULL)),
    CHECK ((current_attempt_id IS NULL) = (lease_until IS NULL))
);
CREATE TABLE attempts (
    id text PRIMARY KEY,
    job_id text NOT NULL REFERENCES jobs(id),
    fence bigint NOT NULL CHECK (fence > 0),
    runner_id text NOT NULL,
    state text NOT NULL CHECK (state IN ('leased','running','uncertain',
                                         'succeeded','failed','cancelled')),
    started_at timestamptz NOT NULL DEFAULT statement_timestamp(),
    finished_at timestamptz,
    UNIQUE (job_id, fence),
    UNIQUE (job_id, id)
);
ALTER TABLE jobs ADD CONSTRAINT current_attempt_belongs_to_job
    FOREIGN KEY (id, current_attempt_id) REFERENCES attempts(job_id, id)
    DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX jobs_ready ON jobs
    (project_id, pool_id, priority DESC, ready_at, id)
    WHERE state = 'queued';
