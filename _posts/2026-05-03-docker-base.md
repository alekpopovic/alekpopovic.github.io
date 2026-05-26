---
layout: post
title: "docker-base"
description: "A Dockerfile-based repository for reusable container foundations and deployment experiments."
category: Public repo
stack: Dockerfile
lib_url: https://github.com/alekpopovic/docker-base
permalink: /posts/docker-base/
---

`docker-base` is a public Dockerfile repository for container foundations. Base images are small pieces of infrastructure design: they encode assumptions about runtime, packages, security posture, and deployment repeatability.

Keeping that work in a repo makes the operational baseline visible. It also makes it easier to reuse the same container decisions across more than one project.
