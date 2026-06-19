<!--
  TEMPLATE: sprint-retrospective  (TIER: premium)
  A structured retrospective on a sprint or milestone. Schema-enforced essay
  scaffold; see templates/free/field-note.md for the field contract.
-->
---
layout: essay
title: "{{Sprint {N} retrospective: {theme} — 10 to 200 chars}}"
author: "@4444J99"
date: "{{YYYY-MM-DD}}"
tags: [retrospective, sprint, {{theme-tag}}]
category: "meta-system"
excerpt: "{{50-400 chars: what the sprint set out to do and the single most important thing you learned.}}"
portfolio_relevance: "MEDIUM"
related_repos:
  - organvm-v-logos/essay-pipeline
reading_time: "{{N}} min"
word_count: {{INTEGER >= 500}}
references: []
---

# {{TITLE}}

## What we set out to do

The sprint goal as stated at the start — not as rationalized afterward. Quote
the original intent.

## What actually shipped

The honest inventory. Link each delivered item to its artifact.

- [x] {{Shipped — link}}
- [ ] {{Did not ship — why}}

## What surprised us

The gap between plan and reality. The unplanned work that ate the budget; the
thing that turned out easier than feared.

## What we are changing

Concrete, owned actions — not vague resolutions. Each one should be checkable at
the next retrospective.

1. {{Change — and how we will know it worked.}}

## Carry-forward

Open threads entering the next sprint, with their current state.

<!-- Cite any referenced reports or dashboards in `references:` above. -->
