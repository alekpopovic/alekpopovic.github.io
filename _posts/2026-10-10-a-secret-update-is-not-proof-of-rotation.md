---
layout: post
title: "A secret update is not proof of rotation"
description: "Object versions, credential validity and workload adoption describe different events. A restart policy needs to say which one it observes."
category: Reliability
book_id: secret-contract-operator
chapter_slug: 13-rotacija-i-rollout
illustration: clock
tags: [secrets, rotation, kubernetes, rollout, identity]
---

A platform team changes a label on a Secret. The operator observes a new resource version and requests a rollout. Someone calls this a false rotation event.

The label update was real. The confusion comes from treating an object change as evidence that a credential changed.

## Name the event you can observe

Separate three facts: the Secret object changed, a synchronization process completed, and the credential provider rotated the actual credential. They can occur at different times, and one does not establish all the others.

A restart token built from the Secret UID and observed resource version identifies an object observation. It avoids placing credential material or a digest of that material into a workload annotation.

That design may restart on approved metadata changes too. Document the behavior as restart on approved object change, rather than promising value-only detection that the token cannot provide.

## Validate before requesting replacement

Imagine the latest Secret is missing a required key. Replacing every healthy application instance would turn a configuration fault into an immediate outage.

The proposed contract workflow reports the failed validation and leaves the restart annotation untouched. Its decision concerns whether to request a new rollout; it cannot guarantee that existing pods will remain alive.

A node failure can independently recreate a pod, which may then consume the invalid Secret. For a stronger handover, consider immutable, versioned Secret objects and an explicit switch of references after validation. That introduces a separate lifecycle to design and test.

## Preserve application ownership

Requesting a rollout should respect the workload's supported update strategy. The application owner decides availability parameters; a credential operator should not quietly rewrite them to make its own operation appear successful.

Define unsupported strategies explicitly. A changed template is not evidence that every pod was replaced, and a replaced pod is not evidence that the external provider accepts its credential.

## Exercise the uncomfortable transitions

Test a metadata-only update, an invalid new value, deletion and recreation of the Secret, and the first enabling of automatic restart. The last case matters because adding the initial token can itself change the workload template.

Then test several updates during an active rollout. Decide how the pending latest observation is reconciled after restart or recovery, rather than emitting an uncontrolled stream of patches.

The resulting policy should explain exactly which observation triggered each action and which later facts still need confirmation.
