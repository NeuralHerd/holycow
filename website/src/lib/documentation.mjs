import path from 'node:path';
import { fileURLToPath } from 'node:url';

export const repository = 'https://github.com/NeuralHerd/holycow';
export const repositoryRoot = fileURLToPath(new URL('../../../', import.meta.url));

export function documentId(entry) {
  if (entry === 'README.md') return 'docs/getting-started';
  return entry.replace(/^website\/src\/content\//, '')
    .replace(/^evals\//, 'docs/evaluations/')
    .replace(/\/SKILL\.md$/, '')
    .replace(/\.md$/, '');
}

export function documentTitle(entry) {
  return entry.body?.match(/^# (.+)$/m)?.[1] ?? entry.id.split('/').at(-1);
}

export function sourceUrl(filePath) {
  const relative = path.relative(repositoryRoot, path.resolve(repositoryRoot, 'website', filePath));
  return `${repository}/blob/main/${relative}`;
}

export function documentationLinks() {
  return (tree, file) => {
    function walk(node) {
      if (node.type === 'link' && !/^(?:[a-z]+:|\/|#)/i.test(node.url)) {
        const [target, fragment] = node.url.split('#');
        const relative = path.relative(repositoryRoot, path.resolve(path.dirname(file.path), target));
        const suffix = fragment ? `#${fragment}` : '';
        node.url = relative.endsWith('.md')
          ? `/${documentId(relative)}/${suffix}`
          : `${repository}/${target.endsWith('/') ? 'tree' : 'blob'}/main/${relative}${suffix}`;
      }
      node.children?.forEach(walk);
    }
    walk(tree);
  };
}
