import { mysqlTable, varchar, int, text, timestamp, json } from 'drizzle-orm/mysql-core';

export const postsMeta = mysqlTable('posts_meta', {
  id: varchar('id', { length: 36 }).primaryKey(),
  slug: varchar('slug', { length: 255 }).unique().notNull(),
  likes: int('likes').default(0),
  createdAt: timestamp('created_at').defaultNow(),
  category: varchar('category', { length: 50 }).default('novedad'),
  title: varchar('title', { length: 255 }),
  description: text('description'),
});

export const comments = mysqlTable('comments', {
  id: varchar('id', { length: 36 }).primaryKey(),
  author: varchar('author', { length: 100 }).notNull(),
  content: text('content').notNull(),
  createdAt: timestamp('created_at').defaultNow(),
  postId: varchar('post_id', { length: 36 }).references(() => postsMeta.id, {
    onDelete: 'cascade'
  }),
});

export const services = mysqlTable('services', {
  id: varchar('id', { length: 36 }).primaryKey(),
  title: varchar('title', { length: 255 }).notNull(),
  description: text('description').notNull(),
  order: int('sort_order').default(0),
});

export const projects = mysqlTable('projects', {
  id: varchar('id', { length: 36 }).primaryKey(),
  title: varchar('title', { length: 255 }).notNull(),
  description: text('description').notNull(),
  image: varchar('image_url', { length: 500 }).notNull(),
  tags: json('tags').$type<string[]>(),
  tech: json('tech').$type<{label: string, value: string}[]>(),
  color: varchar('color', { length: 7 }),
  order: int('sort_order').default(0),
});

export const certifications = mysqlTable('certifications', {
  id: varchar('id', { length: 36 }).primaryKey(),
  name: varchar('name', { length: 255 }).notNull(),
  logo: varchar('logo_url', { length: 500 }),
  order: int('sort_order').default(0),
});