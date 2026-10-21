# Publishing this website

This website is an Astro static build, designed for **Cloudflare Workers Static Assets** at `holycow.neuralherd.dev`.

Cloudflare recommends Workers Static Assets for new static websites. Requests served as static assets are free and unlimited, and asset storage has no additional charge. This site has no Worker script, server rendering, database, or paid service dependency. See [Cloudflare's recommendation](https://developers.cloudflare.com/workers/best-practices/workers-best-practices/) and [static asset pricing](https://developers.cloudflare.com/workers/static-assets/billing-and-limitations/).

Free Workers Builds currently includes 3,000 build minutes per month, one concurrent build, and a 20-minute build timeout. The documentation site should fit comfortably within that allowance under ordinary use. Check the [current limits](https://developers.cloudflare.com/workers/ci-cd/builds/limits-and-pricing/) before changing the build or adding services.

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

## Connect GitHub to Cloudflare

After the website changes are pushed to GitHub:

1. In Cloudflare, open **Workers & Pages → holycow → Settings → Builds** and connect the existing Worker to the `NeuralHerd/holycow` GitHub repository. Limit the GitHub app's repository access to this repository.
2. Select `main` as the production branch and `website` as the project root.
3. Use `npm run verify` as the build command and `npx wrangler deploy` as the deploy command. Set the build environment's Node version to `24.15.0` if it does not pick up `.node-version`.
4. Use the committed `wrangler.jsonc`. It names the Worker `holycow`, publishes only `dist`, and attaches `holycow.neuralherd.dev` as a custom domain.
5. Enable automatic builds for `main`. Leave other branch builds disabled unless preview deployments are wanted.
6. Deploy, then check the custom domain and the generated `workers.dev` address. Confirm the successful build shows the commit pushed to `main`.

Git integration rebuilds the site when changes are pushed to the selected branch. Build from the entire repository: the website reads Markdown outside the `website` directory. If you configure build watch paths, include `skills/**`, `docs/**`, `evals/**`, `README.md`, and `website/**`.

After the connection is enabled, publishing a docs or skill update only requires committing and pushing it to `main`. Cloudflare installs the locked dependencies, runs verification, and deploys only after verification succeeds. Check the Worker's **Deployments** tab for the build result; a failed build leaves the previous deployment live. This uses Cloudflare Workers Builds, so no GitHub Actions deployment workflow or GitHub deployment secret is needed.

See [Cloudflare's Git integration documentation](https://developers.cloudflare.com/workers/ci-cd/builds/).

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
