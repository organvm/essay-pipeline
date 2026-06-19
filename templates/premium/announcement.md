<!--
  TEMPLATE: announcement  (TIER: premium)
  A launch / release announcement that stays substantive instead of hype.
  Schema-enforced essay scaffold; see templates/free/field-note.md.
-->
---
layout: essay
title: "{{Announcing {thing}: {what it does} — 10 to 200 chars}}"
author: "@4444J99"
date: "{{YYYY-MM-DD}}"
tags: [announcement, release, {{product-tag}}]
category: "engineering"
excerpt: "{{50-400 chars: what shipped, who it is for, and why it matters now.}}"
portfolio_relevance: "HIGH"
related_repos:
  - organvm-v-logos/essay-pipeline
  - {{organvm-…/the-released-repo}}
reading_time: "{{N}} min"
word_count: {{INTEGER >= 500}}
references: []
---

# {{TITLE}}

## What shipped

The headline, stated plainly. One paragraph a busy reader can quote.

## Who it is for

Name the user and the job-to-be-done. If everyone is the audience, no one is.

## Why now

The problem that made this worth building, and what was blocking it until now.

## How to use it

The shortest path from reading this to seeing it work.

```bash
{{install / invoke command}}
```

## What it does not do yet

The roadmap honesty section. Known gaps, and what you are deliberately not
solving. This is what separates an announcement from an ad.

## Try it

The single clear call to action and where to send feedback.

<!-- Cite the release tag, changelog, or docs in `references:` above. -->
