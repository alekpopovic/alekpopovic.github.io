---
layout: post
title: "A fast cache is not a release artifact"
description: "Build speed and release identity solve different problems. Keeping them separate makes the pipeline easier to trust."
category: Delivery
book_id: modern-ci
chapter_slug: 14-artifacts-cache
illustration: package
tags: [artifacts, cache, supply chain, builds, retention]
---

A release pipeline restores a warm cache, finishes quickly, and passes its tests. A week later, the cache is evicted and nobody can identify the exact package that went to production.

The problem started when temporary acceleration became the record of a release.

## Give outputs an identity

An artifact is an output that another job or operator can refer to deliberately. Its manifest should connect the bytes to a project, producing attempt, logical name, digest, size, and retention rule.

A downstream job imports that identified output. It does not search a shared directory and hope the latest file is the one intended by the pipeline.

A cache has a different contract. Its absence may make a build slower, but it should not change whether the declared sources can produce the required result. Eviction is an expected behavior, not an unexpected loss of release history.

## Put trust in the cache key's neighborhood

A dependency key can match across a public contribution build and a privileged release build. That does not mean both builds should be allowed to write to the same trusted cache namespace.

Consider the producer's permissions and source trust as well as the dependency identity. Separate less-trusted writers from release inputs, and enforce the separation in the service that stores the cache.

An empty-cache rebuild is a useful experiment. It reveals whether the pipeline depends on undeclared files accumulated by previous jobs. Passing that experiment does not prove every supply-chain property, but it removes one source of hidden state.

## Retain what is still deployed

A production release can outlive the build run's default retention period. If an operator needs to redeploy its artifact, deleting it because the run is old defeats the release record.

Track active release references before making artifacts eligible for collection. Delete in bounded batches and keep a record of the retention action. This makes an intentional deletion distinguishable from unexplained storage loss.

## Review the producer and the bytes

A content digest identifies bytes and helps detect corruption. It does not establish that an authorized, trusted producer created them. Keep provenance and authorization alongside the digest.

At the next pipeline review, choose one production release and follow its artifact backward to the producing attempt. Then rebuild with an empty cache. Those two paths should tell a consistent story: what was released, who produced it, and which shortcuts merely made the work faster.
