# 19. Diagnose failures in the right order

## Start with the visible outcome

A visitor receives 403. First determine whether Nginx's guard denied the request or the protected application returned it. Use the event's guard outcome and an upstream correlation identifier. If the outcome is `block`, inspect the local revision and matching decision. If the outcome is `allow`, investigate application authorization rather than deleting guard state.

A visitor receives an error while the agent is unavailable. Check local process state, socket existence and permissions, first-policy readiness, and time health. Do not begin by tuning detector thresholds. The detector's intent cannot fix a missing request-time dependency.

## Follow an absent ban through the pipeline

If an expected block does not happen, ask a sequence of concrete questions. Did the request finish and produce an access event? Did the collector read the correct file? Did normalization retain the correct site and address? Did ingestion commit it? Was it fresh and eligible? Did the rule threshold actually meet distinct-path criteria? Did central create a decision? Did an edge apply the corresponding revision? Was the site in enforce mode? Was an allowlist or bypass taking precedence?

This sequence separates missing observation from missing delivery and from correct non-enforcement. The answer may simply be that the site is in monitor mode. It may be that a shared address has a deliberate exemption. Removing safeguards to make a demo "work" obscures the actual cause.

## Read errors as protocol information

A signature failure suggests altered bytes, the wrong signing key, an incorrect domain, or a bad encoding. An epoch failure suggests mismatched provisioning. A stale revision after database restore suggests a high-water recovery problem. A same-revision conflict suggests a sender reused a revision for different content.

These are different incidents. Retrying an epoch mismatch forever is not useful. Disabling verification to accept a policy is not a repair. The lab delivery process stops on non-retryable control errors and asks for inspection; a production dispatcher should surface the same distinction in delivery state and alerts.

## Safe local recovery

If the guard is harming availability, activate the documented local bypass through the controlled administrative path. Record why it was activated and make its state visible. Preserve evidence before changing central policy. Revoke harmful decisions or correct mode and allowlist configuration, then reconcile and confirm local application before removing bypass.

Do not delete the state file as a routine "unblock" command. That loses revision history and can leave a new agent not-ready. Do not reset the epoch without a controlled provisioning action. Do not edit the stored signed payload in place: it invalidates the signature and destroys the evidence of what was applied.

## Diagnose collector backlog

When central ingestion recovers, watch buffer occupancy, oldest-event age, accepted-event rate, duplicates, and stale-event exclusions. A rapidly falling buffer is not automatically healthy if valid records are being permanently dropped. A burst of duplicates may be normal recovery from lost acknowledgements. A burst of conflicts is not.

Check rotation and disk capacity before changing retry settings. If unread logs have already been removed, retrying transport cannot reconstruct them. Use the unique request-ID reconciliation from the collection lesson to distinguish duplicate delivery from actual observation loss.

## A concise incident record

Record the affected site, visible outcome, local revision, desired revision, clock health, mode, bypass state, relevant decision expiry, transport condition, and changes made. This small set of facts makes the next investigation faster without dumping raw secrets into the incident channel.

The appendix runbook gives command-oriented steps for the laboratory. A production runbook should add service names, ownership, escalation, backup locations, certificate rotation, and a tested recovery path for your host distribution. Keep it versioned with the deployment artifacts.

## Exercise

Central shows a revoked decision, but one edge still returns 403. List three plausible explanations and the evidence that distinguishes them.

## Answer

The edge may not have applied the newer policy; compare desired and local revision. A different active decision may match the same address; inspect the full desired and local explanation. The application may be returning 403 while the guard allows; inspect the guard outcome and upstream trace. Each explanation leads to a different action, so a generic "clear cache" step is inappropriate.
