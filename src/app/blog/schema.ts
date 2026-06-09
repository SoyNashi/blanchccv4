import { mysqlTable, varchar, int, text, timestamp } from 'drizzle-orm/mysql-core';

export const postsMeta = mysqlTable('posts_meta', {
  id: varchar('id', { length: 36 }).primaryKey(),
  slug: varchar('slug', { length: 255 }).unique().notNull(),
  likes: int('likes').default(0),
  createdAt: timestamp('created_at').defaultNow(),
});

export const comments = mysqlTable('comments', {
  id: varchar('id', { length: 36 }).primaryKey(),
  postSlug: varchar('post_slug', { length: 255 }).references(() => postsMeta.slug),
  author: varchar('author', { length: 100 }).notNull(),
  content: text('content').notNull(),
  createdAt: timestamp('created_at').defaultNow(),
});