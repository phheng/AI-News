---
name: content-factory-workflow-skill
description: Three-stage content pipeline based on the content-factory use case (Research -> Writing -> Creative). Used to produce stable, traceable outputs into Obsidian via cron or manual runs.
version: 1.0.0
task_code: 106-A
language: en
---

# Content Factory Workflow Skill (English)

## Goal
Split content production into 3 independently iterable stages:
1. Research
2. Writing
3. Creative

Ensure outputs are structured, traceable, and reviewable.

## Directory Convention
- Research output: `obsidian-vault/20-Content-Factory/Research/Research-YYYY-MM-DD.md`
- Writing output: `obsidian-vault/20-Content-Factory/Writing/Writing-YYYY-MM-DD.md`
- Creative output: `obsidian-vault/20-Content-Factory/Creative/Creative-YYYY-MM-DD.md`

## Trigger Modes
- Scheduled (cron): run stages in fixed daily slots
- Manual: run any stage on demand

## Stage Requirements

### 1) Research
Minimum output:
- 5 topic candidates
- At least 1 source URL per topic
- Audience, value angle, and risk notes for each topic

### 2) Writing
Input: latest Research file
Minimum output:
- 1 core draft (article/thread)
- 3 title options
- Key claims traceable to Research sources

### 3) Creative
Input: latest Writing file
Minimum output:
- 3 creative concepts
- Each concept includes: headline, subheadline, visual direction, CTA

## Quality Gates
- No source-less conclusions
- No `~` path writes; absolute path only
- Keep outputs concise and execution-oriented

## Failure Fallback
- If one stage fails, do not block unrelated tasks; record failure state
- Prioritize retry on failed stage in next run
- Trigger human check after 3+ consecutive failures

## Source
- usecase: https://github.com/hesamsheikh/awesome-openclaw-usecases/blob/main/usecases/content-factory.md
- raw: https://raw.githubusercontent.com/hesamsheikh/awesome-openclaw-usecases/main/usecases/content-factory.md
