# marketplace-skills

> 日本語版は [README.ja.md](README.ja.md) を参照してください。

A [GitHub Copilot CLI](https://docs.github.com/en/copilot/concepts/agents/about-copilot-cli)
**plugin marketplace**: skills that guide publishing solutions to the
**Microsoft Commercial Marketplace**.

> **EXPERIMENTAL.** These are guided-onboarding skills, not production products. They prepare
> submission-ready packages and checklists. Account guidance never submits or signs in for you.
> Partner Center Onboarding also has an optional publisher-side MCP workflow: human authentication
> and separate preview/confirmation for every change are required. No cloud resources are deployed
> without explicit confirmation.

## Who this is for

Built for anyone working through Partner Center toward publishing on the Microsoft
Commercial Marketplace:

- **Software companies and startups (SDC/ISV)** onboarding to Partner Center and the
  Marketplace for the first time.
- **Anyone helping those teams get set up** — for example a partner manager,
  solution architect, or consultant supporting several companies at once.

Everything here is grounded in **public Microsoft documentation** — no insider
tools or private data — so you can read, share, and build on it freely, whether
you're the company publishing or the person helping them publish.

### Who this is not for

If your company is already onboarded and signed up in Partner Center, or already
has an Offer live on the Marketplace — or you're the Microsoft contact for such a
company — you may not need account guidance. Authorized publishers can separately opt into the
Partner Center Onboarding plugin's Marketplace Ingestion workflow. Partners helping others
publish may still find the guidance useful.

The content is deliberately organized as small, focused skills rather than one
large document, and captures the practical points that are easy to miss — what each
Partner Center review step actually asks for, and country-specific company checks
(in Japan, for example, submitting your official company registry extract and
matching your registered address exactly).

## Plugins in this marketplace

| Plugin | Purpose |
| --- | --- |
| [`agent-publishing`](plugins/agent-publishing) | Publish & monetize Microsoft 365 Copilot agents (declarative, custom engine, Copilot Studio multitenant) |
| [`partner-center-onboarding`](plugins/partner-center-onboarding) | Guidance-only registration/verification + optional Marketplace Ingestion MCP workflow with separately approved publisher operations (live Cowork auth untested) |

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
