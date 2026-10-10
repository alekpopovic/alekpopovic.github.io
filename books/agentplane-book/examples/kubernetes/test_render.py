# SPDX-License-Identifier: MIT
import unittest
from render import render

class ManifestTests(unittest.TestCase):
    def test_restricted(self):
        # This is a syntactic fixture, not a real pullable image.
        m=render("example.invalid/runtime@sha256:"+"a"*64,"reviewed-runtime","v1.35")
        pod=m["items"][-1]["spec"]
        self.assertFalse(pod["automountServiceAccountToken"])
        self.assertEqual(pod["runtimeClassName"],"reviewed-runtime")
        self.assertEqual(pod["securityContext"]["seccompProfile"]["type"],"RuntimeDefault")
        self.assertTrue(pod["containers"][0]["securityContext"]["readOnlyRootFilesystem"])
        self.assertFalse(pod["containers"][0]["securityContext"]["allowPrivilegeEscalation"])
        self.assertEqual(m["items"][2]["spec"]["egress"],[])
    def test_tags_rejected(self):
        for image in ["busybox:latest","busybox:1.0","x@sha256:123","x;echo x"]:
            with self.assertRaises(ValueError): render(image,"runtime","v1.35")
    def test_runtime_validation(self):
        for runtime in ["", "../x", "x_unsafe", "a"*64]:
            with self.assertRaises(ValueError):
                render("example.invalid/x@sha256:"+"a"*64,runtime,"v1.35")
    def test_policy_version(self):
        with self.assertRaises(ValueError):
            render("example.invalid/x@sha256:"+"a"*64,"runtime","latest")
if __name__=="__main__": unittest.main()
