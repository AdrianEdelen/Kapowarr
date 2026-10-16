# deadbolt fork of Kapowarr

This fork's `main` is upstream [Casvt/Kapowarr](https://github.com/Casvt/Kapowarr)
`development` plus our fixes that upstream hasn't merged yet. It is what the
deadbolt home server runs, as `ghcr.io/adrianedelen/kapowarr:deadbolt`.

The aim is for `main` to differ from upstream as little as possible: every fix
here is written so it can be sent upstream unchanged, and stops being ours once
upstream merges it.

## Day to day

**A new fix**

```bash
git fetch upstream
git switch -c patch/<topic> upstream/development   # from upstream, not from main
# change it, add tests, then:
python3 -m unittest discover -s ./tests -p '*.py'
git push -u origin patch/<topic>
gh pr create -R AdrianEdelen/Kapowarr --base main   # -R matters: without it gh targets upstream
```

Review and merge the PR as usual. `deadbolt CI` tests it; merging publishes a new
image, and Renovate in `server-stacks` proposes the new digest.

**Docs go in the same branch.** If a fix changes something `docs/` describes,
update `docs/` in that fix branch. Our docs then differ from upstream's exactly
as long as the code does. (The fork doesn't publish a docs site: upstream's
`deploy.yml` is disabled here, and Kapowarr's in-app help links to upstream's
site regardless.)

**Why branch from `upstream/development`, not `main`?** So that the branch holds
only that fix. The same branch can then become an upstream PR as it is, without
dragging our other changes or these fork-only files along.

**Upstream changes** arrive as a daily `Sync upstream development` PR opened by
`deadbolt upstream sync`, already tested. Merge it like any other PR. If it
conflicts, the run fails and says so; merge `upstream/development` into a branch
from `main` locally, resolve, and open the PR by hand.

**Never click "Update branch"** on a fix PR. It merges `main` into the fix
branch, which makes it no longer upstreamable.

## Sending a fix upstream

Upstream asks for an approved
[contribution request](https://github.com/Casvt/Kapowarr/issues/new?template=3_contribute_request.yml)
before a PR ([CONTRIBUTING.md](https://github.com/Casvt/Kapowarr/blob/development/CONTRIBUTING.md)).

```bash
git switch patch/<topic>
git fetch upstream && git rebase upstream/development
git push --force-with-lease
```

Then open the PR from `AdrianEdelen:patch/<topic>` to `Casvt:development`. Review
changes go on the same branch. Once upstream merges it, the next sync brings
their copy into `main` and the branch can be deleted.

## What's in main beyond upstream

`git log --oneline upstream/development..main --no-merges` lists it. The
fork-only files are this one and `.github/workflows/deadbolt-*.yml`. Upstream's
own `deploy.yml` is disabled on this fork. Upstream's other branches aren't
mirrored here; use the `upstream` remote
(`git remote add upstream https://github.com/Casvt/Kapowarr.git`).
