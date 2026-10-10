---
layout: post
title: "Your access log does not need that token"
description: "Useful security observations start with a deliberate field list, before credentials and visitor data spread through the pipeline."
category: Security
book_id: logbranik
chapter_slug: 05-logs-without-secrets
illustration: logs
tags: [nginx, access logs, privacy, tokens, normalization]
---

A visitor follows a password-reset link. The application handles the request correctly, but the full URL enters an access log. The reset token now travels through a collector, a queue, an analysis database, and perhaps a troubleshooting export.

None of those systems needed the token to count failed requests. They received it because the logging contract was broader than the question being asked.

## Start with the detector's question

For a baseline request detector, useful fields include a generated request identity, event time, site, resolved client address, method, query-free path, status, duration, byte count, and guard outcome.

Authorization headers, session cookies, request bodies, and query strings should not appear merely because they are available. Requiring a purpose for each field keeps the observation pipeline easier to operate and limits the places sensitive data can accumulate.

Removing a field at the source is different from promising to clean it up after ingestion. Later cleanup cannot undo the copies that have already passed through other systems.

## A path can still identify somebody

Dropping the query string does not make every route harmless. A path such as `/customers/123456/profile` can carry an identifier of its own.

Review the application's routes. Where appropriate, normalize selected paths to a route pattern at a trusted stage, or exclude a route that the detector does not need. Preserve the signal required by the rule without treating every URL shape as equally suitable for retention.

## Preserve the outcome that produced the status

An application 403 and a security guard's 403 mean different things. If a detector counts its own denied requests as new hostile evidence, a short restriction can feed itself.

Record whether the guard allowed, blocked, would have blocked, bypassed, or could not decide. In the book's teaching rule, only observations with an `allow` outcome contribute to fresh detection.

Also test internal redirects and location-specific access-log rules. The original path and final outcome should still describe one public request, rather than a convenient intermediate step in Nginx routing.

## Inspect the record at every boundary

Send a controlled request containing a fake token and a path with a sample identifier. Inspect the edge log, normalized event, stored observation, and any diagnostic export.

The result should match the field contract at every stage. A logging policy becomes useful when the actual bytes follow it, including when a request takes an error path.
