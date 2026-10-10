# 15. Build once and preserve the image digest


## Reuse a builder rather than inventing one

Modern CI orchestrates image builds through BuildKit. BuildKit already provides a build graph, caching, and image-output machinery; the platform's responsibility is to constrain inputs, assign authority, record outputs, and surface failures. The upstream project documents its execution and cache capabilities. [S09](e-sources.md#s09)

Keep the builder's authority separate from the job container. A job does not need a host Docker socket simply to request a controlled image build. Select an executor arrangement suitable for the trusted-runner boundary and document what the builder can access on that host.

Image construction has phases worth reporting separately: context preparation, source resolution, build execution, export, and optional registry publication. A successful build with a failed registry push is not a published release. Capture the final digest only from a confirmed output operation.

## Make build inputs identifiable

A build record should name source commit, Dockerfile digest, context digest or a defensible context manifest, platform, builder version, declared build parameters, and selected base-image identities where resolved. This does not magically make arbitrary network-dependent Dockerfiles reproducible. It identifies what the platform can observe and where uncontrolled inputs remain.

Each application repository owns its Dockerfile and complete build context. A server image build from `apps/server` must not silently copy sibling source from the workspace. Resolve versioned modules or prepare a verified vendor snapshot before the build. A convenient root context can conceal that an application is not independently releasable.

Exclude credentials, local configuration, `.git` content when unnecessary, and oversized directories with an appropriate `.dockerignore`. Review what actually enters the context rather than relying only on intent.

## Distinguish registry cache from artifact storage

Docker documents multiple cache backends, including a registry backend. The availability of a particular backend depends on the builder configuration. S3-compatible storage for platform artifacts does not mean the same deployment automatically supports every BuildKit cache mode. [S10](e-sources.md#s10)

Begin with an explicitly configured registry cache under project and trust-scoped references. Readers and writers should have different grants where appropriate. Cache failures can degrade performance without turning a successful build into an unverifiable output, provided the build remains correct without the cache.

Do not inject secrets through build arguments or permanent environment layers. Docker's build-secret mechanism provides temporary secret mounts intended for the build operation. The Dockerfile and builder still decide how that secret is used; granting it to untrusted build logic remains unsafe. [S11](e-sources.md#s11)

## Promote the artifact, not the source branch

Once a tested image digest exists, deployment should reference that digest. Rebuilding the same commit for production can produce different bytes if external dependencies, tags, timestamps, or network results change. Build once and promote the confirmed artifact through environments, recording each approval and target observation.

For a multi-platform image, record whether the release identity is an image index or a platform-specific manifest. The target adapter must verify that the selected runtime platform is supported. Avoid using a local image ID as though it were the published registry digest.

A release manifest can include provenance information, but provenance is evidence about a build process, not a universal statement that the output is safe. Tie it to the builder identity and verification policy, then retain the corresponding source and test records.

## Exercise

Staging runs `application:latest`. Production rebuilds the same commit and also runs `application:latest`. Both deployments succeed. Has the team demonstrated that production uses the bytes tested in staging?

## Worked answer

No. The tag is mutable, and a second build may resolve different inputs. Record the finalized registry digest from the first build and promote that exact identity. Verify the target's observed digest after rollout. Source equality and tag equality are weaker than artifact identity.

## Completion evidence

Test independent build contexts, secret handling, cache isolation, export versus push failure, architecture mismatch, digest capture, and promotion without rebuilding. Do not claim registry publication was tested unless it actually occurred in an authorized test registry.
