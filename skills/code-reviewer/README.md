# Code Reviewer

Senior engineer conducting thorough, constructive code reviews that improve code quality and share knowledge.

## What This Skill Does

- Reviews pull requests for correctness, security, performance, and maintainability
- Identifies critical issues, major concerns, and minor improvement opportunities with prioritized feedback
- Validates test coverage and test quality alongside production code
- Checks for security vulnerabilities aligned with OWASP Top 10 and common anti-patterns
- Provides actionable suggestions with concrete code examples, not just complaints
- Produces structured review reports with a clear verdict (approve, request changes, or comment)

## Installation

### Option 1: .skill file

Create a file called `code-reviewer.skill` in your project root:

```
url = https://github.com/jeffallan/claude-skills/tree/main/skills/code-reviewer
```

### Option 2: Copy the folder

Copy the `skills/code-reviewer` folder into your project's `.claude/skills/` directory:

```bash
cp -r skills/code-reviewer .claude/skills/code-reviewer
```

## What's Included

```
code-reviewer/
├── SKILL.md
├── README.md
└── references/
    ├── common-issues.md
    ├── feedback-examples.md
    ├── receiving-feedback.md
    ├── report-template.md
    ├── review-checklist.md
    └── spec-compliance-review.md
```

## Example Prompts

```
Review this pull request and flag any security or performance issues. Focus on the
database access layer changes.
```

```
Conduct a code quality audit on the authentication module. Check for OWASP Top 10
vulnerabilities and suggest refactoring opportunities.
```

## Platform Compatibility

| Platform     | Supported |
|--------------|-----------|
| Claude Code  | Yes       |
| Cursor       | Yes       |
| Windsurf     | Yes       |

## Related Skills

- **Security Reviewer** - Deep security-focused analysis beyond general code review
- **Test Master** - Dedicated test quality assessment and coverage analysis
- **Architecture Designer** - Higher-level design and architectural review
