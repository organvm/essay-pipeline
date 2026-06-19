<!--
  TEMPLATE: field-note  (TIER: free)
  A short, single-claim essay scaffold. This is the free sample from the
  essay-pipeline template library — copy it, fill the {{TOKENS}}, and it will
  pass `essay-validate` against the editorial-standards frontmatter schema.

  Schema contract enforced below (essay layout):
    layout              must be "essay"
    title               10-200 chars
    author              "@4444J99"
    date                YYYY-MM-DD
    tags                2-8 items, lowercase-hyphenated  ^[a-z0-9]+(-[a-z0-9]+)*$
    category            one of the editorial-standards categories
    excerpt             50-400 chars, one paragraph
    portfolio_relevance CRITICAL | HIGH | MEDIUM
    related_repos       repo paths matching ^(organvm-|meta-organvm)
    reading_time        "N min"  (~ word_count / 250)
    word_count          integer >= 500, matches body
    references          list (may be empty)
-->
---
layout: essay
title: "{{TITLE — 10 to 200 characters, descriptive not clickbait}}"
author: "@4444J99"
date: "{{YYYY-MM-DD}}"
tags: [{{tag-one}}, {{tag-two}}]
category: "meta-system"
excerpt: "{{One-paragraph summary, 50-400 characters, that states the single claim this field note makes.}}"
portfolio_relevance: "MEDIUM"
related_repos:
  - organvm-v-logos/essay-pipeline
reading_time: "{{N}} min"
word_count: {{INTEGER >= 500}}
references: []
---

# {{TITLE}}

> One field note = one observation, defended in a few hundred words. Keep it
> tight. If you need sections and sub-arguments, reach for a premium template.

## The observation

State what you saw, plainly. One claim. {{What happened, where, when.}}

## Why it holds

Give the evidence. Concrete and specific — names, numbers, a trace. Do not
generalize past what you can support.

## What it implies

One paragraph on the consequence. Be honest about the limits of the claim.

<!--
  Validate before publishing:
    essay-validate --posts-dir <dir-with-this-file>/ \
      --schema ../editorial-standards/schemas/frontmatter-schema.yaml
-->
