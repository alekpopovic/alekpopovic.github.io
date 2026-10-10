# Restricted Kubernetes Manifest Lab

The renderer outputs JSON, which Kubernetes accepts as an object representation.
It does **not** call kubectl, install a runtime or run a container. Choose a real,
reviewed OCI image digest, installed RuntimeClass and supported Pod Security
version in your disposable environment.

```sh
python3 examples/kubernetes/render.py --help
python3 -m unittest discover -s examples/kubernetes -v
```

Generate a manifest by supplying all three required arguments. Inspect the output
before any manual apply. The image's configured entrypoint runs as UID 10001;
it must support that identity and the limited writable paths. There is no DNS or
internet allowance. Test fixtures use `example.invalid` and are not pullable.

The default-deny NetworkPolicy needs an enforcing CNI. Restricted pod settings
and a RuntimeClass name do not prove hostile-code containment. The ordinary Pod
here is a small teaching specimen, not the production Agent Sandbox adapter.
Do not deploy it to a shared or production cluster. Its workspace is ephemeral.
