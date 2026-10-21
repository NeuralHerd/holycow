# HolyCow website

Astro static documentation for `https://holycow.neuralherd.dev`, hosted on Cloudflare Workers Static Assets.

```sh
cd website
npm ci
npm run dev
```

Use Node.js 24.15.0 (see `.node-version`). Run `npm run verify` before deployment. It checks types, builds all pages, and checks internal links and anchors. Build output is `dist/`.

The site reads skill instructions, references, the root README, and public docs directly from this repository. Human introductions and example prompts live in `src/data/skills.ts`; they should be reviewed alongside changes to skill behavior.

Pushes to `main` run the [deployment workflow](../.github/workflows/deploy-website.yml), which verifies and deploys the website. See [publishing instructions](src/content/docs/hosting.md) for GitHub Actions setup, free hosting, the custom domain, and manual deployment. A local build does not publish the site or change DNS.
