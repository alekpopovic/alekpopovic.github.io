# 27. Deliver One Complete Vertical Slice

**Part VIII — Implementation and Publication**

The capstone is not the entire product. It is a narrow, observable path through
all important trust boundaries. A fictional Northstar developer creates one
session, runs one harmless command and requests one governed tool operation in a
local cluster. A second tenant tries to observe or repeat that work and fails.

## Define the demonstration contract

The developer must authenticate, select an organization and project, and submit
a session request using a reviewed runtime-template version. The API returns an
operation identifier. A local connector receives a typed command over an
authenticated connection and checks the cluster-local policy envelope before
creating the approved upstream resource.

Readiness requires a working execution path, not simply a pod phase. The operator
can explain the image digest, runtime class, namespace, effective network policy
and credential bindings. Unsupported capabilities are shown as unavailable;
there is no default-runtime fallback hidden beneath a secure-profile label.

## Execute a harmless workload

Run a fixed program that prints a short message and writes a small workspace
file. Download the file through the authorized transfer path and compare its
checksum. Try a path outside the workspace and verify rejection. Do not use real
customer repositories or production credentials for the first demonstration.

Interrupt the client stream. The execution record should remain meaningful even
when output delivery stops. Reconnect only according to the supported stream
contract. Do not promise full replay of output that was intentionally not stored.

## Govern one tool operation

Register a local test tool that modifies only a disposable test record. Discovery
must not enable it. Confirm default denial, create a policy requiring approval
and submit an operation bound to exact actor, tenant, project, session, tool,
input digest and policy version.

Approve through a different authorized identity when four-eyes review is enabled.
Attempt to reuse the approval, change the input and call the tool directly around
the gateway. A convincing demonstration observes each rejection at the actual
enforcement point, not only in a console notification.

## Add failure before adding features

Disconnect the connector after intent is committed. Show the last observed state
and its age. Verify that the local lifetime still bounds the workload. Restart
the connection and reconcile without creating a second session for the same
operation. Revoke credentials and verify both central rejection and the stated
limits of disconnected local enforcement.

Exercise a duplicate usage event. The aggregate must not increase twice. Attempt
cross-tenant audit export and event subscription. Test these with the actual
application identity rather than an administrator connection.

## Produce a review packet

The packet should contain the architecture revision, exact dependency manifest,
commands run, safe test outputs, known gaps and the mapping from every advertised
property to evidence. Include the restore plan before inviting external users.
A short video can explain the workflow, but it cannot replace these records.

The accompanying capstone lab supplies acceptance criteria rather than a claim
that this repository already contains the full application. The teaching programs
are smaller building blocks. Their value is to make key invariants executable
before integrating cloud, database and cluster systems.

## Grow only from observed demand

After the vertical slice, choose the next capability from customer evidence.
Some customers will value governance and audit more than warm pools. Others need
a direct data path before they can try the product. A third group may require
stronger runtime isolation or a dedicated installation.

Do not add GPU scheduling, a billing provider and a marketplace simply because
they fit the architectural diagram. Each creates a new operational contract.
The next feature should have a buyer, a boundary and an acceptance test.

## Exercise

Write a ten-minute demonstration script and a separate acceptance-test list. Mark
which steps are storytelling and which provide machine-checkable evidence.
Explain what the product must show when termination is requested during a cluster
partition. A polished spinner is not an acceptable answer.
