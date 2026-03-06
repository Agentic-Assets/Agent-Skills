# MCP Developer

Build MCP servers and clients that connect AI systems with external tools and data sources using the Model Context Protocol.

## What This Skill Does

- Guides implementation of MCP servers using the TypeScript or Python SDKs
- Designs protocol-compliant resources, tools, and prompt templates with proper schemas
- Enforces JSON-RPC 2.0 protocol correctness across stdio, HTTP, and SSE transports
- Applies input validation (Zod/Pydantic), authentication, rate limiting, and security controls
- Helps debug protocol compliance issues and optimize MCP performance
- Provides deployment guidance for packaging, configuring, and monitoring MCP servers in production

## Installation

### Option 1: .skill file

Create a file called `mcp-developer.skill` in your project root:

```
/skills/mcp-developer
```

Then configure your agent to load skills from the [Agent Skills registry](https://github.com/jeffallan/claude-skills).

### Option 2: Copy the folder

Copy the `skills/mcp-developer` folder directly into your project's skills directory:

```bash
cp -r skills/mcp-developer /path/to/your/project/skills/
```

## What's Included

```
skills/mcp-developer/
├── SKILL.md                          # Core skill definition and workflow
├── README.md                         # This file
└── references/
    ├── protocol.md                   # Message types, lifecycle, JSON-RPC 2.0
    ├── typescript-sdk.md             # Building servers/clients in Node.js
    ├── python-sdk.md                 # Building servers/clients in Python
    ├── tools.md                      # Tool definitions, schemas, execution
    └── resources.md                  # Resource providers, URIs, templates
```

## Example Prompts

1. **"Build an MCP server in TypeScript that exposes our PostgreSQL database as resources and provides query tools for Claude."**
   Triggers the full workflow: requirement analysis, resource URI design, tool schema definition, and server implementation with the TypeScript SDK.

2. **"I'm getting JSON-RPC errors when my MCP client connects to the server over stdio. Help me debug the protocol handshake."**
   Loads protocol reference to diagnose message lifecycle issues, transport configuration, and version compatibility problems.

## Platform Compatibility

| Platform | Supported |
|----------|-----------|
| Claude Code | Yes |
| Cursor | Yes |
| Windsurf | Yes |
| Cline | Yes |
| Other agents supporting .skill files | Yes |

## Related Skills

- **FastAPI Expert** - Python API servers for HTTP transport
- **TypeScript Pro** - Advanced TypeScript for Node.js servers
- **Security Reviewer** - Security audits for MCP implementations
- **DevOps Engineer** - Deployment and monitoring
