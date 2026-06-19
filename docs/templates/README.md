# Essay Template Library

The essay-pipeline ships a catalog of **schema-enforced essay templates** — the
same structural contracts the pipeline validates against, packaged as ready-to-
fill scaffolds. Copy a template, replace the `{{TOKENS}}`, and it passes
`essay-validate` against the editorial-standards frontmatter schema on the first
try.

One **free sample** is included. The rest are **premium**, unlocked once with a
one-time-purchase license key — no subscription, no activation server.

## Catalog

| Template | Tier | Price | Best for |
| -------- | ---- | ----- | -------- |
| **Field Note** (`field-note`) | Free | — | Short, single-claim observations |
| **Building-in-Public Case Study** (`case-study`) | Premium | bundle | Documenting a piece of work end to end |
| **Technical Deep Dive** (`technical-deep-dive`) | Premium | bundle | Explaining how a component actually works |
| **Sprint Retrospective** (`sprint-retrospective`) | Premium | bundle | Closing a sprint with plan-vs-reality honesty |
| **Release Announcement** (`announcement`) | Premium | bundle | Shipping something and saying why it matters |
| **Argument Essay** (`argument-essay`) | Premium | bundle | Taking a defensible position |

The canonical machine-readable catalog is [`templates/manifest.yaml`](../../templates/manifest.yaml).

## Pricing

| SKU | What you get | Price |
| --- | ------------ | ----- |
| `premium-single` | Any one premium template | **$49** |
| `premium-bundle` | All premium templates + every future addition | **$99** |

One-time purchase. Each sale issues a license key tied to the buyer's email.

## How it works

```
buy ──▶ seller runs `essay-license issue` ──▶ you receive a key
                                                     │
                          `essay-template list --license KEY`  (premium shows "unlocked")
                          `essay-template eject case-study --output my-essay.md --license KEY`
```

### 1. Browse (no key needed)

```bash
essay-template list
```

Free templates show `open`; premium templates show `locked`.

### 2. Read or copy a template

```bash
# Free — works with no key:
essay-template show field-note

# Premium — requires a valid license key:
essay-template eject case-study --output drafts/my-case-study.md --license EPK1.XXXX.YYYY
```

Without a valid key, premium templates exit with `LOCKED` and a pointer back to
this catalog.

### 3. Fill and validate

Replace every `{{TOKEN}}`, then validate before publishing:

```bash
essay-validate --posts-dir drafts/ \
  --schema ../editorial-standards/schemas/frontmatter-schema.yaml
```

## Licensing model (HMAC key check)

License keys are signed with **HMAC-SHA256** over a readable payload
(`sku | email | issued`). Verification is fully offline — the same shared
secret signs and verifies. See [`src/license.py`](../../src/license.py) and the
architecture note in
[`docs/adr/003-template-library-licensing.md`](../adr/003-template-library-licensing.md).

**For sellers.** Set a private signing secret and issue keys with it:

```bash
export ESSAY_PIPELINE_LICENSE_SECRET="your-long-random-private-secret"
essay-license issue --email buyer@example.com --sku premium-bundle
# → EPK1.GEZDGNBV.MFRGGZDF...   (give this to the buyer)
```

**For buyers.** Verify a key you received:

```bash
essay-license verify --key EPK1.GEZDGNBV.MFRGGZDF...
```

> **Security note.** This is a deterrent-grade gate, not DRM: anyone holding the
> secret can mint keys, and an offline check can be bypassed by editing the
> source. That is an accepted trade-off for a no-server, one-time-purchase
> product. Protect the secret; rotate it (and re-issue keys) if it leaks. A
> hardened deployment would move to asymmetric signatures or online activation.
