import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { documentId } from './lib/documentation.mjs';

const documentation = defineCollection({
  loader: glob({
    base: new URL('../../', import.meta.url),
    pattern: ['README.md', 'skills/**/*.md', 'docs/*.md', 'evals/*.md', 'website/src/content/docs/*.md'],
    generateId: ({ entry }) => documentId(entry),
  }),
});

export const collections = { documentation };
