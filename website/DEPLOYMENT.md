# Publishing this website

This website is an Astro static build, designed for **Cloudflare Workers Static Assets** at `holycow.neuralherd.dev`.

Cloudflare recommends Workers Static Assets for new static websites. Requests served as static assets are free and unlimited, and asset storage has no additional charge. This site has no Worker script, server rendering, database, or paid service dependency. See [Cloudflare's recommendation](https://developers.cloudflare.com/workers/best-practices/workers-best-practices/) and [static asset pricing](https://developers.cloudflare.com/workers/static-assets/billing-and-limitations/).

GitHub Actions builds and deploys this site. Standard GitHub-hosted runners are free for public repositories; private repositories use the account's included Actions allowance. See [GitHub Actions billing](https://docs.github.com/en/billing/concepts/product-billing/github-actions).

## Preview locally

From the repository root, with Node.js 24.15.0 or a compatible version:

```sh
cd website
npm ci
npm run dev
```

The development server prints the local preview address. For a production check:

```sh
npm run verify
npm run preview
```

Verification checks Astro types, builds the static pages, and checks internal page links and anchors. The deployable output is `website/dist`.

## Automatic deployment from GitHub

The `Deploy website` workflow in `.github/workflows/deploy-website.yml` runs on pushes to `main`. It installs the locked dependencies, runs `npm run verify`, and deploys with `npx wrangler deploy` only after verification succeeds. It uses Node.js from `website/.node-version` and builds from the entire repository because the website reads Markdown outside `website`.

Repository setup under **Settings → Secrets and variables → Actions**:

- Add the repository secret `CLOUDFLARE_API_TOKEN` with the restricted deployment token.
- Add the repository variable `CLOUDFLARE_ACCOUNT_ID` with the Cloudflare account ID that owns `holycow` and `neuralherd.dev`.

The deployment token needs **Workers Scripts: Edit** and **Account Settings: Read** in that account; **Workers Routes: Edit** and **Zone: Read** only for `neuralherd.dev`; and **User Details: Read** and **Memberships: Read**. It needs no database, storage, queue, or AI permissions. Store its value only in the repository secret. To rotate it, replace that secret and rerun the workflow.

After setup, publish a docs or skill update by committing and pushing to `main`. Check **Actions → Deploy website** for the result and confirm the run shows the expected commit. You can also use **Run workflow** with `main` to redeploy. A failed verification leaves the previous deployment live. Keep Cloudflare's separate Git builds disconnected to avoid duplicate deployments.

The committed `wrangler.jsonc` names the Worker `holycow`, publishes `dist`, and attaches `holycow.neuralherd.dev`. See [Cloudflare's GitHub Actions documentation](https://developers.cloudflare.com/workers/ci-cd/external-cicd/github-actions/).

## Connect holycow.neuralherd.dev

The `neuralherd.dev` zone must be active in the same Cloudflare account.

The custom domain is declared in `wrangler.jsonc`, so deployment attaches it automatically. You can verify the mapping in the deployed Worker's **Domains** tab:

```text
holycow.neuralherd.dev
```

Cloudflare creates the DNS record and provisions a TLS certificate for the custom domain. You do not need a separate certificate subscription. If that hostname already has a DNS record, inspect what uses it before replacing it; Cloudflare does not allow a custom domain on an existing CNAME.

Verify HTTPS, a skill page, a reference page, and a nonexistent URL after the domain becomes active. The last should show the site's 404 page.

See [Cloudflare custom domains](https://developers.cloudflare.com/workers/configuration/routing/custom-domains/). A local build does not change DNS; publishing applies the configured domain.

## Deploy from your machine instead

From `website`, sign in to your Cloudflare account and deploy:

```sh
npx wrangler login
npm run deploy
```

The deploy command verifies the site first and applies the custom domain configured above. Never commit account credentials or API tokens.

## Keep the docs in sync

- Skill pages render `skills/*/SKILL.md` and their Markdown references directly.
- Getting started renders the root `README.md`.
- Attribution, the design review, and evaluation scenarios render their existing repository files.
- Short skill introductions and sample prompts live in `website/src/data/skills.ts`.
- Website-specific guides live in `website/src/content/docs/`.

Update the short introduction if a skill's purpose changes, and add a catalogue entry when adding a skill. The build rewrites repository Markdown links to the matching website pages. Source and edit links return to GitHub.

## Could this use GitHub Pages?

Yes. The static output is portable. GitHub Pages supports custom domains and is free for public repositories on GitHub Free. Private-repository Pages availability depends on the GitHub plan. You would add a Pages deployment workflow and configure the domain and DNS for Pages instead.

For this project, Cloudflare keeps the domain, HTTPS, and deployment in the account already managing the DNS. See [GitHub Pages availability](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages).
