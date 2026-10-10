# SPDX-License-Identifier: MIT
"""Render a teaching List; never connect to or mutate a Kubernetes cluster."""
from __future__ import annotations
import argparse
import json
import re

LABEL = {"app.kubernetes.io/name": "agentplane-book-example"}

def render(image: str, runtime: str, policy_version: str) -> dict:
    if not re.fullmatch(r"[a-zA-Z0-9][a-zA-Z0-9._:/-]*@sha256:[a-f0-9]{64}",image):
        raise ValueError("an explicit OCI reference with SHA-256 digest is required")
    if len(runtime)>63 or not re.fullmatch(r"[a-z0-9](?:[a-z0-9-]*[a-z0-9])?",runtime):
        raise ValueError("use a valid, already installed RuntimeClass name")
    if not re.fullmatch(r"v1\.[0-9]+",policy_version):
        raise ValueError("pin the Pod Security version, for example v1.<minor>")
    ns="agentplane-book-lab"
    items=[
      {"apiVersion":"v1","kind":"Namespace","metadata":{"name":ns,"labels":{
        "pod-security.kubernetes.io/enforce":"restricted",
        "pod-security.kubernetes.io/enforce-version":policy_version}}},
      {"apiVersion":"v1","kind":"ServiceAccount","metadata":{"name":"workload","namespace":ns},
       "automountServiceAccountToken":False},
      {"apiVersion":"networking.k8s.io/v1","kind":"NetworkPolicy",
       "metadata":{"name":"default-deny","namespace":ns},
       "spec":{"podSelector":{},"policyTypes":["Ingress","Egress"],"ingress":[],"egress":[]}},
      {"apiVersion":"v1","kind":"Pod","metadata":{"name":"example","namespace":ns,"labels":LABEL},
       "spec":{"runtimeClassName":runtime,"serviceAccountName":"workload",
        "automountServiceAccountToken":False,"restartPolicy":"Never",
        "activeDeadlineSeconds":300,
        "securityContext":{"runAsNonRoot":True,"runAsUser":10001,"runAsGroup":10001,
          "fsGroup":10001,"seccompProfile":{"type":"RuntimeDefault"}},
        "containers":[{"name":"example","image":image,"imagePullPolicy":"IfNotPresent",
          "securityContext":{"allowPrivilegeEscalation":False,"readOnlyRootFilesystem":True,
            "capabilities":{"drop":["ALL"]}},
          "resources":{"requests":{"cpu":"100m","memory":"64Mi"},
             "limits":{"cpu":"500m","memory":"256Mi","ephemeral-storage":"128Mi"}},
          "volumeMounts":[{"name":"workspace","mountPath":"/workspace"},
                          {"name":"tmp","mountPath":"/tmp"}]}],
        "volumes":[{"name":"workspace","emptyDir":{"sizeLimit":"64Mi"}},
                   {"name":"tmp","emptyDir":{"medium":"Memory","sizeLimit":"32Mi"}}]}}
    ]
    return {"apiVersion":"v1","kind":"List","items":items}
if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--image",required=True)
    parser.add_argument("--runtime-class",required=True)
    parser.add_argument("--policy-version",required=True)
    args=parser.parse_args()
    try:
        print(json.dumps(render(args.image,args.runtime_class,args.policy_version),indent=2))
    except ValueError as exc:
        parser.error(str(exc))
