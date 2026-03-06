# Debugging Wizard

Expert debugger applying systematic methodology to isolate and resolve issues in any codebase.

## What This Skill Does

- Investigates errors, exceptions, and unexpected behavior using a structured reproduce-isolate-hypothesize-test-fix workflow
- Analyzes stack traces and error messages to pinpoint root causes
- Diagnoses intermittent issues, race conditions, and memory leaks
- Guides performance debugging and profiling across languages and frameworks
- Provides structured output including root cause, evidence, fix, and prevention steps
- Loads specialized reference material for debugging tools, common patterns, strategies, and quick fixes based on context

## Installation

### Option 1: .skill file

Create a file called `debugging-wizard.skill` in your project root:

```
/skills/debugging-wizard
```

Then point it to this skill's location or add it as a dependency in your agent configuration.

### Option 2: Copy folder

Copy the entire `debugging-wizard` folder into your project's skills directory:

```
cp -r skills/debugging-wizard /path/to/your/project/skills/
```

## What's Included

```
debugging-wizard/
├── SKILL.md
├── README.md
└── references/
    ├── common-patterns.md
    ├── debugging-tools.md
    ├── quick-fixes.md
    ├── strategies.md
    └── systematic-debugging.md
```

## Example Prompts

**Investigating a runtime error:**

> My API is returning a 500 error on the `/users` endpoint. Here's the stack trace from the logs. Can you help me find the root cause and fix it?

**Diagnosing an intermittent failure:**

> Our CI tests pass locally but fail randomly in the pipeline. The failure is in the database integration tests and seems to happen about 30% of the time. Help me debug this.

## Platform Compatibility

| Platform       | Supported |
|----------------|-----------|
| Claude Code    | Yes       |
| Cursor         | Yes       |
| Windsurf       | Yes       |
| Cline          | Yes       |
| Other MCP agents | Yes    |

## Related Skills

- **Test Master** - Writing regression tests after fixing bugs
- **Fullstack Guardian** - Implementing fixes across the stack
- **Monitoring Expert** - Setting up alerting to catch issues early
