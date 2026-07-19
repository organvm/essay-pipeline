[![ORGAN-V: Logos](https://img.shields.io/badge/ORGAN--V-Logos-0d47a1?style=flat-square)](https://github.com/organvm-v-logos)
[![CI](https://github.com/organvm-v-logos/essay-pipeline/actions/workflows/ci.yml/badge.svg)](https://github.com/organvm-v-logos/essay-pipeline/actions/workflows/ci.yml)
[![Tier: Standard](https://img.shields.io/badge/tier-standard-blue?style=flat-square)](https://github.com/organvm-iv-taxis/orchestration-start-here)

# essay-pipeline

_Essay automation engine for the ORGAN-V discourse layer_

---

## What It Is

essay-pipeline is the automation backbone behind ORGAN-V's public-process discourse layer. Where [public-process](https://github.com/organvm-v-logos/public-process) is the published surface -- the Jekyll site hosting essays, sprint narratives, and meta-system reflections -- essay-pipeline is the machinery underneath: Python CLIs and GitHub Actions workflows that convert system activity into publishable editorial artifacts.

The pipeline monitors cross-organ signals such as promotions, CI passes, new repositories, dependency changes, and milestone completions. It turns those signals into structured essay-topic suggestions, sprint narrative drafts, schema-validated markdown, link-check reports, and JSON indexes for the public site.

This repo does not contain the published essays themselves. It contains the tools that make essay production systematic, consistent, and traceable:

- `essay-suggest` generates ranked topic suggestions from corpus gaps, surfaced reading, and cross-reference signals.
- `essay-narrate` drafts sprint narratives from analytics and publication cadence data.
- `essay-draft` uses an LLM provider to turn a selected topic into a schema-compliant draft.
- `essay-validate`, `essay-index`, and `link-check` keep the corpus publishable.
- `essay-template` and `essay-license` package the same schema contract as a one-time-purchase template library.

The design philosophy is automation-as-infrastructure: essay-pipeline should be quiet when working correctly and loud when something breaks. Frontmatter that does not conform to schema fails validation. Sprint narratives that lack required sections are caught before publication. Indexes are rebuilt from content instead of hand-maintained.

## Who Pays

The open-source pipeline is infrastructure for ORGAN-V and can be run by anyone who has the required input repositories and data files. The monetized product is the template library, not a hosted service and not access to the validator or indexer.

The paying customer is an author, maintainer, research group, or building-in-public team that wants ready-to-fill, schema-enforced essay templates without assembling an editorial system from scratch. They pay once for a license key that unlocks premium templates locally.

The operator or seller pays for their own runtime costs: GitHub Actions minutes, repository hosting, optional LLM API usage, and any payment processing. Buyers bring their own LLM/API keys if they use `essay-draft`; the template library itself has no activation server and no recurring billing.

## Install

Prerequisites:

- Python 3.10+
- Git
- For the full ORGAN-V workflow: local access to `public-process`, `editorial-standards`, analytics data, and surfaced-reading feeds
- For LLM drafting only: an API key for Anthropic, OpenAI, Gemini, Perplexity, or a local Ollama setup

Install from a checkout:

```bash
git clone https://github.com/organvm-v-logos/essay-pipeline.git
cd essay-pipeline
python3 -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
```

Verify the console scripts are available:

```bash
essay-validate --help
essay-template list
```

For template-library use without test tooling, `pip install -e .` is enough.

## Usage

Validate essays or logs against the canonical schemas:

```bash
essay-validate \
  --posts-dir ../public-process/_posts/ \
  --schema ../editorial-standards/schemas/frontmatter-schema.yaml

essay-validate \
  --posts-dir ../public-process/_logs/ \
  --schema ../editorial-standards/schemas/log-schema.yaml \
  --content-type log
```

Rebuild public-process data artifacts:

```bash
essay-index \
  --posts-dir ../public-process/_posts/ \
  --logs-dir ../public-process/_logs/ \
  --output-dir ../public-process/data/
```

Generate weekly intelligence artifacts:

```bash
essay-suggest \
  --essays-index ../public-process/data/essays-index.json \
  --xrefs ../public-process/data/cross-references.json \
  --tag-governance ../editorial-standards/schemas/tag-governance.yaml \
  --category-taxonomy ../editorial-standards/schemas/category-taxonomy.yaml \
  --surfaced ../reading-observatory/feeds/surfaced.json \
  --output data/topic-suggestions.json

essay-narrate \
  --metrics ../analytics-engine/data/engagement-metrics.json \
  --report ../analytics-engine/data/system-engagement-report.json \
  --index ../public-process/data/essays-index.json \
  --calendar ../public-process/data/publication-calendar.json \
  --output data/sprint-narrative-draft.md
```

Draft an essay from a suggestion:

```bash
export LLM_PROVIDER="anthropic"
export ANTHROPIC_API_KEY="..."

essay-draft \
  --suggestions data/topic-suggestions.json \
  --suggestion-index 0 \
  --template-dir ../editorial-standards/templates/ \
  --schema ../editorial-standards/schemas/frontmatter-schema.yaml \
  --rubric ../editorial-standards/schemas/quality-rubric.yaml \
  --tag-governance ../editorial-standards/schemas/tag-governance.yaml \
  --category-taxonomy ../editorial-standards/schemas/category-taxonomy.yaml \
  --posts-dir ../public-process/_posts/ \
  --output-dir drafts/
```

Use the template library:

```bash
essay-template list
essay-template show field-note
essay-license issue --email buyer@example.com --sku premium-bundle
essay-template eject case-study --output drafts/my-case-study.md --license EPK1.XXXX.YYYY
```

## Architecture

The current pipeline is implemented as composable CLI modules:

```
reading-observatory feeds + analytics-engine data + public-process corpus
                    |
                    v
      topic_suggester + sprint_narrator (weekly intelligence artifacts)
                    |
                    v
                 essay_drafter (LLM draft generation + repair)
                    |
                    v
          validator + indexer + link_checker (quality gates)
                    |
                    v
           public-process content + data updates + log scaffolds
```

## Components

### `src/topic_suggester.py`

Generates scored, ranked essay-topic suggestions from corpus gaps, surfaced reading items, and cross-reference gaps.

### `src/sprint_narrator.py`

Builds a markdown sprint narrative from analytics metrics, engagement report data, index data, and publication cadence.

### `src/essay_drafter.py`

Generates full essay drafts from topic suggestions using configured LLM providers, validates schema compliance, and applies deterministic frontmatter repairs.

### `src/validator.py`

Validates essay/log frontmatter against canonical schemas in `editorial-standards/schemas/`. Validation is strict: required fields, optional-field types, cross-field checks, and unknown-field rejection are enforced.

### `src/indexer.py`

Indexes essays and logs into JSON artifacts consumed by `public-process/data/`.

### `src/log_generator.py`

Scans workspace or GitHub activity and scaffolds daily captain's logs plus activity JSON snapshots.

### `src/link_checker.py`

Extracts and validates markdown links (internal + external) and emits structured reports for CI/QA use.

### `src/llm_client.py`

Provider-agnostic client layer for Anthropic, OpenAI, Gemini, Perplexity, and Ollama.

## Frontmatter Schema

Canonical schema files live in:
- `../editorial-standards/schemas/frontmatter-schema.yaml`
- `../editorial-standards/schemas/log-schema.yaml`

Essay frontmatter (required keys):
- `layout`, `title`, `author`, `date`, `tags`, `category`, `excerpt`
- `portfolio_relevance`, `related_repos`, `reading_time`, `word_count`, `references`

Optional integrity keys:
- `word_count_policy`, `word_count_override_reason`

Unknown frontmatter keys are rejected by the validator to prevent schema drift.

## Pricing / Monetization

essay-pipeline monetizes the schema-enforced template library. The automation CLIs remain open-source infrastructure; buyers pay for curated, ready-to-fill writing scaffolds that already satisfy the pipeline's publication contract.

| Tier / SKU | Price | Access | Buyer fit |
| ---------- | ----- | ------ | --------- |
| Free sample | $0 | `field-note` template, no license key | Try the format and validate a simple essay |
| `premium-single` | $49 one-time | One selected premium template sold from the catalog | Authors who need one repeatable format |
| `premium-bundle` | $99 one-time | Full premium catalog plus future premium additions | Teams that publish multiple essay types |

The premium catalog currently includes case studies, technical deep dives, sprint retrospectives, release announcements, and argument essays. The canonical tier/pricing source is `templates/manifest.yaml`; the buyer-facing catalog is [docs/templates/README.md](docs/templates/README.md).

Fulfillment is intentionally simple:

1. Buyer purchases a premium SKU.
2. Seller runs `essay-license issue --email buyer@example.com --sku premium-bundle` with a private `ESSAY_PIPELINE_LICENSE_SECRET`.
3. Buyer receives an `EPK1.<payload>.<signature>` key.
4. Buyer passes the key to `essay-template show` or `essay-template eject`.

There is no subscription, account system, or activation server. License verification is an offline HMAC-SHA256 check implemented in `src/license.py`, and premium reads are gated in `src/template_store.py`. This is a deterrent-grade license gate for an open-source repo, not DRM; the commercial value is the editorial structure, curation, and convenience of the template set.

Useful commands:

```bash
essay-template list
essay-template list --license EPK1.XXXX.YYYY
essay-template show field-note
essay-template eject case-study --output drafts/my-case-study.md --license EPK1.XXXX.YYYY
essay-license verify --key EPK1.XXXX.YYYY
```

References:

- Catalog and buyer instructions: [docs/templates/README.md](docs/templates/README.md)
- Machine-readable manifest: `templates/manifest.yaml`
- Storefront/gate: `src/template_store.py`
- License keys: `src/license.py`
- Licensing rationale: [docs/adr/003-template-library-licensing.md](docs/adr/003-template-library-licensing.md)

## Workflow Integration

Active repository workflows:

### Weekly Intelligence (`.github/workflows/weekly-intelligence.yml`)

Generates:
- `data/topic-suggestions.json`
- `data/sprint-narrative-draft.md`

Uses:
- `src.topic_suggester`
- `src.sprint_narrator`

### Essay Generation (`.github/workflows/essay-generation.yml`)

Generates and validates draft essays from topic suggestions using:
- `src.essay_drafter`
- `src.validator`

### Daily Captain's Log (`.github/workflows/daily-log.yml`)

Builds daily log scaffolds and activity snapshots with:
- `src.log_generator`

### CI (`.github/workflows/ci.yml`)

Runs lint/test validation for the package and repo structure checks.

## Data Contracts

Surfaced-reading input contract (producer: `reading-observatory`, consumer: `essay-pipeline`):
- [docs/data-contract-surfaced-items.md](docs/data-contract-surfaced-items.md)

## Development

Use the install flow above with `pip install -e .[dev]` before running tests or lint checks.

### Environment Variables

```bash
export LLM_PROVIDER="anthropic"        # optional, auto-detected when unset
export ANTHROPIC_API_KEY="..."         # or OPENAI_API_KEY / GEMINI_API_KEY / PERPLEXITY_API_KEY
export GITHUB_TOKEN="..."              # required only for github-api mode in log_generator
```

### Testing

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=src --cov-report=term-missing

# Run specific test module
pytest tests/test_validator.py -v
```

### Project Structure

```
essay-pipeline/
  .github/
    workflows/
      ci.yml
      weekly-intelligence.yml
      essay-generation.yml
      daily-log.yml
  docs/
    adr/
      ...
    data-contract-surfaced-items.md
  src/
    essay_drafter.py
    indexer.py
    link_checker.py
    llm_client.py
    log_generator.py
    schema_loader.py
    sprint_narrator.py
    topic_suggester.py
    validator.py
  tests/
    test_*.py
    fixtures/
  CHANGELOG.md
  LICENSE
  README.md
  pyproject.toml
  seed.yaml
```

## How It Fits the System

essay-pipeline is part of the organvm eight-organ creative-institutional system:

| Organ | Name | Domain | Relationship to essay-pipeline |
|-------|------|--------|-------------------------------|
| I | Theoria | Foundational theory and recursive structures | Referenced in essay topics and narratives |
| II | Poiesis | Creative production and artistic works | Source material for case studies and retrospectives |
| III | Ergon | Practical applications and tools | Source material for implementation essays |
| IV | Taxis | Orchestration, governance, infrastructure | Upstream workflow and governance context |
| **V** | **Logos** | **Public process, discourse, essays** | **This repo. Automation engine for the discourse layer.** |
| VI | Koinonia | Community and collaboration | Input for community-facing narrative context |
| VII | Kerygma | Proclamation and external communication | Consumes essay outputs for distribution |
| META | meta-organvm | Cross-organ umbrella | System-wide governance and structural context |

essay-pipeline exists because a system of 80+ repositories across 8 organizations generates too much activity for manual essay curation. The pipeline turns upstream data and editorial standards into validated drafts, narratives, logs, and indexes that remain machine-readable and publishable.

## Design Principles

The pipeline is built on three guiding principles that inform every implementation decision:

**Automation as infrastructure.** The pipeline should be invisible when working correctly. No human should need to remember to run the indexer after publishing an essay, or manually scan eight organizations for essay topics. If a process can be triggered automatically, it must be. Manual intervention is reserved for editorial decisions -- choosing which topics to write about, shaping narrative voice, deciding publication timing.

**Strict schemas with explicit evolution.** Every data contract in the pipeline is formally defined and enforced. Frontmatter fields are validated against a schema. Event scoring uses documented weights. Index structure follows a versioned format. When something needs to change, the change goes through an ADR, not through a quick edit that silently alters behavior. This strictness is a feature: it makes the system predictable and auditable.

**Cross-organ awareness without cross-organ coupling.** Intelligence modules consume cross-organ data but publish only into ORGAN-V artifacts. This read-many/write-few pattern keeps the blast radius contained.

## Contributing

Contributions follow the [organvm contribution guidelines](https://github.com/organvm-v-logos/.github/blob/main/CONTRIBUTING.md).

Key points for this repo:

1. **Schema changes** require an ADR in `docs/adr/` before implementation
2. **Data contract changes** must update producer/consumer docs and tests
3. **Workflow changes** should be validated against relevant fixtures and local command runs
4. **All Python code** must pass `ruff check` with zero warnings

To propose a new frontmatter field:
1. Open an issue describing the field, its type, and why it is needed
2. Draft an ADR following the template in `docs/adr/`
3. Implement the field in `../editorial-standards/schemas/frontmatter-schema.yaml` and `src/validator.py`
4. Update the README's Frontmatter Schema section
5. Open a PR referencing the issue and ADR

## License

[MIT](./LICENSE) -- see LICENSE file for full text.

---

_LOGOS Sprint -- organvm-v-logos/essay-pipeline -- February 2026_
