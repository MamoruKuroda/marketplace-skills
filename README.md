# marketplace-skills

> 日本語版は [README.ja.md](README.ja.md) を参照してください。

A [GitHub Copilot CLI](https://docs.github.com/en/copilot/concepts/agents/about-copilot-cli)
**plugin marketplace**: skills that guide publishing solutions to the
**Microsoft Commercial Marketplace**.

> **EXPERIMENTAL.** These are guided-onboarding skills, not production products. They prepare
> submission-ready packages and checklists; they never submit to Partner Center for you, and never
> deploy cloud resources without explicit confirmation.

## Plugins in this marketplace

| Plugin | Purpose |
| --- | --- |
| [`agent-publishing`](plugins/agent-publishing) | Publish & monetize Microsoft 365 Copilot agents (declarative, custom engine, Copilot Studio multitenant) |

Planned: `saas-publishing`, `container-publishing`, `managed-app-publishing`.

## Install

This repository is itself a Copilot CLI plugin marketplace (it contains
`.github/plugin/marketplace.json`). There are two ways to use it.

### A. Register the marketplace, then install a plugin

```bash
copilot plugin marketplace add MamoruKuroda/marketplace-skills
copilot plugin install agent-publishing@marketplace-skills
```

### B. Install a plugin directly from its subdirectory

```bash
copilot plugin install MamoruKuroda/marketplace-skills:plugins/agent-publishing
```

Then verify:

```bash
copilot plugin list
# in an interactive session: /skills list
```

## License

Dual-licensed: **MIT** for code/configuration ([`LICENSE-CODE`](LICENSE-CODE)) and
**Creative Commons Attribution 4.0 (CC-BY-4.0)** for documentation/content ([`LICENSE`](LICENSE)).
Copyright Mamoru Kuroda.
