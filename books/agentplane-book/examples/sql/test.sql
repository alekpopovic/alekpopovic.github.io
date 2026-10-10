-- SPDX-License-Identifier: MIT
\set ON_ERROR_STOP on
BEGIN;
SET LOCAL ROLE agentplane_book_app;
SELECT set_config('app.organization_id','11111111-1111-4111-8111-111111111111',true);
INSERT INTO agentplane_book.sessions VALUES (
 '11111111-1111-4111-8111-111111111111','aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa',
 'cccccccc-cccc-4ccc-8ccc-cccccccccccc','requested');
DO $$
BEGIN
 IF (SELECT count(*) FROM agentplane_book.sessions) != 1 THEN
   RAISE EXCEPTION 'scoped insert/read failed';
 END IF;
 BEGIN
  INSERT INTO agentplane_book.sessions VALUES (
   '22222222-2222-4222-8222-222222222222','bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb',
   'dddddddd-dddd-4ddd-8ddd-dddddddddddd','requested');
  RAISE EXCEPTION 'cross-tenant insert unexpectedly passed';
 EXCEPTION WHEN insufficient_privilege THEN NULL;
 END;
 BEGIN
  INSERT INTO agentplane_book.sessions VALUES (
   '11111111-1111-4111-8111-111111111111','bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb',
   'eeeeeeee-eeee-4eee-8eee-eeeeeeeeeeee','requested');
  RAISE EXCEPTION 'foreign project unexpectedly passed';
 EXCEPTION WHEN foreign_key_violation THEN NULL;
 END;
END $$;
SELECT set_config('app.organization_id','22222222-2222-4222-8222-222222222222',true);
DO $$ BEGIN
 IF (SELECT count(*) FROM agentplane_book.sessions) != 0 THEN
   RAISE EXCEPTION 'cross-tenant read';
 END IF;
END $$;
SELECT set_config('app.organization_id','',true);
DO $$ BEGIN
 IF (SELECT count(*) FROM agentplane_book.sessions) != 0 THEN
   RAISE EXCEPTION 'missing-context read';
 END IF;
END $$;
ROLLBACK;
\echo 'Isolation lab passed; inserted session data rolled back.'
