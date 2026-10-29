---
name: context7-mcp
description: Fetch library and API docs with Context7 when Grounded Docs is unavailable or insufficient, or the user explicitly requests Context7.
---

Prefer Grounded Docs through the configured LiteLLM MCP connection for documentation lookups. Use Context7 only when Grounded Docs is unavailable, lacks the required library/version, or cannot answer after a refined search and relevant page reads, or when the user explicitly requests Context7. Do not call Context7 as a second lookup when Grounded Docs already provides sufficient evidence.

Follow the shared lookup policy in `/Users/damacus/.codex/context7.md`.

## When to Use This Skill

When a fallback is needed, activate this skill for a user who:

- Asks setup or configuration questions ("How do I configure Next.js middleware?")
- Requests code involving libraries ("Write a Prisma query for...")
- Needs API references ("What are the Supabase auth methods?")
- Mentions specific frameworks (React, Vue, Svelte, Express, Tailwind, etc.)

## How to Fetch Documentation

### Step 1: Resolve the Library ID

Call `resolve-library-id` with:

- `libraryName`: The library name extracted from the user's question
- `query`: The user's full question (improves relevance ranking)

### Step 2: Select the Best Match

From the resolution results, choose based on:

- Exact or closest name match to what the user asked for
- Higher benchmark scores indicate better documentation quality
- If the user mentioned a version (e.g., "React 19"), prefer version-specific IDs

### Step 3: Fetch the Documentation

Call `query-docs` with:

- `libraryId`: The selected Context7 library ID (e.g., `/vercel/next.js`)
- `query`: The user's specific question

### Step 4: Use the Documentation

Incorporate the fetched documentation into your response:

- Answer the user's question using current, accurate information
- Include relevant code examples from the docs
- Cite the library version when relevant

## Guidelines

- **Be specific**: Pass the user's full question as the query for better results
- **Version awareness**: When users mention versions ("Next.js 15", "React 19"), use version-specific library IDs if available from the resolution step
- **Prefer official sources**: When multiple matches exist, prefer official/primary packages over community forks
