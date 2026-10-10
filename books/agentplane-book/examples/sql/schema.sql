-- SPDX-License-Identifier: MIT
-- Disposable database only. Execute as an owner allowed to create test roles.
\set ON_ERROR_STOP on
BEGIN;
CREATE ROLE agentplane_book_app NOLOGIN NOSUPERUSER NOBYPASSRLS;
CREATE SCHEMA agentplane_book;
REVOKE ALL ON SCHEMA agentplane_book FROM PUBLIC;
CREATE TABLE agentplane_book.organizations (
 id uuid PRIMARY KEY, name text NOT NULL
);
CREATE TABLE agentplane_book.projects (
 organization_id uuid NOT NULL REFERENCES agentplane_book.organizations(id),
 id uuid NOT NULL,
 PRIMARY KEY (organization_id,id)
);
CREATE TABLE agentplane_book.sessions (
 organization_id uuid NOT NULL,
 project_id uuid NOT NULL,
 id uuid NOT NULL,
 status text NOT NULL CHECK (status IN ('requested','ready','terminated')),
 PRIMARY KEY (organization_id,id),
 FOREIGN KEY (organization_id,project_id)
 REFERENCES agentplane_book.projects(organization_id,id)
);
ALTER TABLE agentplane_book.sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE agentplane_book.sessions FORCE ROW LEVEL SECURITY;
CREATE POLICY tenant_scope ON agentplane_book.sessions
 USING (organization_id = NULLIF(current_setting('app.organization_id', true),'')::uuid)
 WITH CHECK (organization_id = NULLIF(current_setting('app.organization_id', true),'')::uuid);
GRANT USAGE ON SCHEMA agentplane_book TO agentplane_book_app;
GRANT SELECT,INSERT,UPDATE,DELETE ON agentplane_book.sessions TO agentplane_book_app;
INSERT INTO agentplane_book.organizations VALUES
 ('11111111-1111-4111-8111-111111111111','A'),
 ('22222222-2222-4222-8222-222222222222','B');
INSERT INTO agentplane_book.projects VALUES
 ('11111111-1111-4111-8111-111111111111','aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa'),
 ('22222222-2222-4222-8222-222222222222','bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb');
COMMIT;
