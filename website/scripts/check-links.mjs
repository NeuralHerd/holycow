import { readdir, readFile, stat } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = fileURLToPath(new URL('../dist/', import.meta.url));
const files = (await readdir(root, { recursive: true })).filter(file => file.endsWith('.html'));
const documents = new Map();
const failures = [];
let checked = 0;

for (const file of files) {
  const html = await readFile(path.join(root, file), 'utf8');
  const ids = new Set([...html.matchAll(/\bid="([^"]+)"/g)].map(match => match[1]));
  documents.set(file, { html, ids });
}

for (const [file, { html }] of documents) {
  const base = `https://holycow.neuralherd.dev/${file.replace(/index\.html$/, '')}`;
  for (const [, href] of html.matchAll(/\bhref="([^"]+)"/g)) {
    const url = new URL(href.replaceAll('&amp;', '&'), base);
    if (url.origin !== 'https://holycow.neuralherd.dev') continue;
    const pathname = decodeURIComponent(url.pathname).replace(/^\//, '');
    const target = pathname.endsWith('/') || !pathname ? `${pathname}index.html` : pathname;
    let exists = documents.has(target);
    if (!exists) {
      try { exists = (await stat(path.join(root, target))).isFile(); } catch { /* Report the missing target below. */ }
    }
    if (!exists) failures.push(`${file}: missing ${href}`);
    else if (url.hash && documents.has(target) && !documents.get(target).ids.has(decodeURIComponent(url.hash.slice(1)))) {
      failures.push(`${file}: missing anchor ${href}`);
    }
    checked++;
  }
}

if (failures.length) {
  console.error(failures.join('\n'));
  process.exitCode = 1;
} else {
  console.log(`Checked ${checked} internal links and anchors across ${documents.size} pages.`);
}
