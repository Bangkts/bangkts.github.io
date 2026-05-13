import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const articles = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/articles' }),
  schema: z.object({
    title: z.string(),
    category: z.string(),
    categoryOrder: z.number().optional().default(99),
    order: z.number().optional().default(99),
    source: z.string().url().optional(),        // link bài gốc
    sourceLabel: z.string().optional(),         // tên nguồn, vd: "ByteByteGo"
  }),
});

export const collections = { articles };
