# Publish the book repository and website

These steps publish this book, not the production application. The supplied
archive has not created a remote repository. Use a new directory so that you
do not overwrite an existing application's history.

## 1. Create the source repository

Place the contents of the archive's `modern-ci-book/` directory at
the root of the new repository, including `.github/`.

Create an **empty public** GitHub repository named `modern-ci-book` under an
account or organization you control. Do not add a generated README or license:
this package already contains both. Set your real Git identity locally if it
is not configured.

Run from the book directory:

```bash
git init -b main
git add .
git commit -m "Publish Modern CI open edition 0.1"
# Replace YOUR_OWNER after creating the empty repository.
git remote add origin git@github.com:YOUR_OWNER/modern-ci-book.git
git push -u origin main
```

The URL above is a template, not a claim that a repository already exists.
Git authentication must already be configured. `dist/` is excluded by
`.gitignore`; the source remains reviewable without generated binaries.

## 2. Enable GitHub Pages

Open repository **Settings → Pages → Build and deployment** and select
**GitHub Actions** as the source. Under Actions, run **Publish book** manually,
or push a new commit to `main`. The workflow builds reading editions and the
static site, uploads the Pages artifact, and deploys through the
`github-pages` environment.

The actual deployment URL is returned by the workflow. Review repository and
organization policies for Actions and environment approvals. GitHub's
[custom-workflow documentation](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages)
explains Pages permissions, artifacts and deployment environments.

Only the default `main` workflow publishes. Pull requests run read-only checks;
they do not receive Pages deployment permissions. Do not change the workflow
trigger to `pull_request_target` to run untrusted contribution code.

The supplied workflows use official actions at reviewed major-version tags.
These tags are movable references. Before a hardened release, resolve each to
an independently reviewed full commit SHA and record it; no fabricated SHA is
included. Protect `main` and require the validation check before merging.

## 3. Publish reading editions

Run the local release checks and exports. Create a GitHub release for the exact
source commit you reviewed, then attach `modern-ci-book.pdf`,
`modern-ci-book.epub`, and optionally the sample PDF from `dist/`.
Include the edition number, checks performed, known omissions and checksums.
Do not claim that a green publishing workflow validates the production CI/CD
platform described in the book.

## 4. Make a correction

Edit the Markdown source, add or update the companion test where relevant,
update `CHANGELOG.md`, and open a pull request. Regenerate the edition after
review. Material behavior changes should increment `book.json`'s edition and
update citation and release metadata together.

A public book repository is independently useful. Linking to private
application repos does not make those applications open source; publish their
source and suitable licenses separately when ready.
