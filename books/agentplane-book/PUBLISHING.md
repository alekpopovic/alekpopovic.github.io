# Publishing the Book on GitHub

## Prepare your repository

Review the license allocation and maintainer identity. Create an empty GitHub
repository under your own account or organization; `agentplane-book` is a suggested
name, not an existing repository claimed by this edition. Keep this book separate
from a future AgentPlane implementation repository.

Extract the ZIP and inspect its contents, especially workflows. Add a real private
security-reporting route and maintainers before inviting community contributions.
The package includes no `.git` history and performs no remote writes.

## Push only after review

Use your own remote URL; the placeholder below is intentionally not an active URL.

```sh
git init -b main
git add .
git commit -m "docs: publish AgentPlane book edition 0.1.0"
git remote add origin YOUR_OWN_REPOSITORY_REMOTE
git push -u origin main
```

## Enable the website

In repository Settings, open Pages and choose **GitHub Actions** as the build
source. The Pages workflow is manual (`workflow_dispatch`) so publication is an
explicit maintainer action. Its deployment job has only Pages and identity-token
permissions; pull-request validation has no deployment authority.

Run the Pages workflow from the trusted `main` branch after checks pass. Configure
the `github-pages` environment's protection rules and branch restrictions in the
repository. The generated site uses relative paths and does not require a hardcoded
account or repository URL. See the official GitHub Pages source cited in the book.

## Publish reading editions

Run `make book`, inspect PDF pages and validate the EPUB. Attach the files in
`dist/` and the full repository ZIP to a manually reviewed GitHub release. Use a
book tag such as `book-v0.1.0` to avoid confusing it with application versions.
The included workflows do not automatically create GitHub releases.

The initial ZIP includes PDF and EPUB files under `dist/` for convenience.
Maintainers may move large later editions to Release assets; update README links
in that case. Keep individual Markdown chapters in Git.
