# Releasing HolyCow

Installs follow `main`, so every push reaches users who update. A release names a point on `main` with a version, so installed copies, eval results and bug reports can say exactly which skills they used. The version rules are at the top of [CHANGELOG.md](../../CHANGELOG.md).

1. Record changes under `## [Unreleased]` in `CHANGELOG.md` as they land.
2. Choose the next version from those changes, then set it everywhere:

   ```sh
   python3 scripts/set_version.py 0.2.0
   ```

3. Rename `## [Unreleased]` to `## [0.2.0] - <date>`, add a new empty `## [Unreleased]` above it, and update the comparison links at the bottom.
4. Run the checks, which also confirm that `VERSION`, every skill and the changelog agree:

   ```sh
   PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s evals
   ```

5. Commit, tag and push:

   ```sh
   git commit -am "Release 0.2.0"
   git tag -a v0.2.0 -m "HolyCow 0.2.0"
   git push origin main v0.2.0
   ```

6. Create the GitHub release from that changelog section:

   ```sh
   gh release create v0.2.0 --title "HolyCow 0.2.0" --notes-file <(python3 scripts/changelog_section.py 0.2.0)
   ```
