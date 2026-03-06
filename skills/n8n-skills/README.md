# n8n Skills

An AI coding agent skill for building n8n workflows, configuring nodes, setting up triggers, implementing data transformations, and integrating AI agents into automation workflows.

## What This Skill Does

- Provides detailed documentation for 545+ built-in n8n nodes and 30+ community packages
- Helps find the right nodes for specific automation tasks using a categorized index
- Includes 20 ready-to-use workflow templates across AI, social media, data processing, and communication
- Offers node configuration examples and best practices for common workflow patterns
- Covers trigger setup, webhook processing, database synchronization, and email automation
- Guides AI agent and RAG system integration within n8n workflows

## Installation

**Option 1: .skill file**

Add the following to your project's `.skill` file:

```
n8n-skills
```

**Option 2: Copy folder**

Copy the `n8n-skills/` folder into your project's skills directory:

```bash
cp -r n8n-skills /path/to/your/project/skills/
```

## What's Included

```
n8n-skills/
├── SKILL.md
├── README.md
├── references/
│   └── overview.md
└── resources/
    ├── INDEX.md
    ├── compatibility-matrix.md
    ├── community/
    │   ├── README.md
    │   └── ... (30+ community node packages)
    ├── guides/
    │   ├── how-to-find-nodes.md
    │   └── usage-guide.md
    ├── input/
    │   ├── README.md
    │   ├── input-merged.md
    │   └── ... (individual node docs)
    ├── misc/
    │   ├── README.md
    │   └── misc-merged.md
    ├── organization/
    │   ├── README.md
    │   └── organization-merged.md
    ├── output/
    │   ├── README.md
    │   ├── output-merged.md
    │   └── ... (individual node docs)
    ├── templates/
    │   ├── README.md
    │   ├── ai-chatbots/        (15 templates)
    │   ├── social-media/       (1 template)
    │   ├── data-processing/    (3 templates)
    │   └── communication/      (1 template)
    ├── transform/
    │   ├── README.md
    │   └── ... (individual node docs + merged files)
    └── trigger/
        ├── README.md
        ├── trigger-merged.md
        └── ... (individual trigger node docs)
```

## Example Prompts

1. "I need to build an n8n workflow that monitors a Gmail inbox for new emails, classifies them using OpenAI, and sends a summary to Slack."

2. "Help me set up a webhook in n8n that receives order data from Shopify, transforms it, and writes it to a Postgres database on a schedule."

## Platform Compatibility

| Platform       | Supported |
|----------------|-----------|
| Claude Code    | Yes       |
| Cursor         | Yes       |
| Windsurf       | Yes       |
| Cline          | Yes       |
| Custom Agents  | Yes       |

## Related Skills

- [mcp-developer](../mcp-developer/) - For building MCP servers that can integrate with n8n via the MCP community node
- [fastapi-expert](../fastapi-expert/) - For building API backends that n8n workflows can call via HTTP Request nodes
