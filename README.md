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

## Quick start (try it in ~5 minutes)

> Want to publish a Copilot agent to Microsoft Marketplace but not sure where to start?
> These skills interview you, pick the right path, and produce a submission-ready package and
> checklist — so you don't have to memorize the Partner Center flow.

**Prerequisites**

- [GitHub Copilot CLI](https://docs.github.com/en/copilot/how-tos/set-up/install-copilot-cli)
  (`copilot --version`). VS Code Copilot Chat works too.
- For full runs (Azure deploys, packaging): Azure CLI (`az`), GitHub CLI (`gh`), and the
  Microsoft 365 Agents Toolkit CLI (`npm install -g @microsoft/m365agentstoolkit-cli`).
  The guidance/triage skills work without these.

**1. Install Git-Ape (this plugin builds on it)**

```bash
copilot plugin marketplace add Azure/git-ape
copilot plugin install git-ape@git-ape
```

**2. Install this plugin**

```bash
copilot plugin marketplace add MamoruKuroda/marketplace-skills
copilot plugin install agent-publishing@marketplace-skills
```

**3. Verify**

```bash
copilot plugin list          # shows agent-publishing@marketplace-skills
```

In an interactive `copilot` session, `/skills list` should show the eight skills.

**4. Try your first interview**

```text
copilot
> /triage-agent-type I'm a startup building a declarative HR policy agent and I want to charge for it.
```

The triage skill asks a few questions, decides your path, and tells you which skill runs next.
See the [`agent-publishing` plugin README](plugins/agent-publishing/README.md)
([日本語](plugins/agent-publishing/README.ja.md)) for the full walkthrough.

## Install (reference)

This repository is itself a Copilot CLI plugin marketplace (it contains
`.github/plugin/marketplace.json`). Besides the marketplace flow above, you can install a plugin
directly from its subdirectory:

```bash
copilot plugin install MamoruKuroda/marketplace-skills:plugins/agent-publishing
```

## License

Dual-licensed: **MIT** for code/configuration ([`LICENSE-CODE`](LICENSE-CODE)) and
**Creative Commons Attribution 4.0 (CC-BY-4.0)** for documentation/content ([`LICENSE`](LICENSE)).
Copyright Mamoru Kuroda.
