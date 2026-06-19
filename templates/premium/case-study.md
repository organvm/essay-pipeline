<!--
  TEMPLATE: case-study  (TIER: premium)
  A building-in-public case study: problem → approach → result, with the
  receipts. Schema-enforced essay scaffold. See templates/free/field-note.md
  for the full field contract; the same rules apply here.
-->
---
layout: essay
title: "{{How we {outcome}: a {system} case study — 10 to 200 chars}}"
author: "@4444J99"
date: "{{YYYY-MM-DD}}"
tags: [case-study, {{domain-tag}}, {{system-tag}}]
category: "meta-system"
excerpt: "{{50-400 chars: the problem, what you did, and the one result a reader should remember.}}"
portfolio_relevance: "HIGH"
related_repos:
  - organvm-v-logos/essay-pipeline
  - {{organvm-…/relevant-repo}}
reading_time: "{{N}} min"
word_count: {{INTEGER >= 500}}
references: []
---

# {{TITLE}}

## Context

The situation before the work. What was true, what was constraining, and who
cared. Anchor it to a real repo or sprint so it is verifiable.

## The problem

State it as a tension, not a task. What were the two things that could not both
be true? {{e.g. "validation had to be strict, but authors needed fast feedback".}}

## What we tried

The approach, including the parts that did not work. Show the dead ends — a
case study with no failed attempts reads as marketing.

1. {{First move and what it cost.}}
2. {{Second move and what it revealed.}}

## The result

Concrete outcome with numbers where you have them. Tie each claim back to an
artifact (a commit, a CI run, a metric) a reader could inspect.

| Metric | Before | After |
| ------ | ------ | ----- |
| {{…}}  | {{…}}  | {{…}} |

## What transfers

The generalizable lesson — and explicitly, its boundary. Where would this
approach stop working?

<!-- Add cited sources to `references:` above when you reference external work. -->
