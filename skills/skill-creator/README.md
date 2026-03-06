# Skill Creator

Create new skills, modify existing skills, and measure skill performance through an iterative eval-driven workflow.

## What This Skill Does

- Guides you through the full skill authoring lifecycle: capturing intent, writing the SKILL.md, and bundling resources
- Generates test prompts and runs them with and without the skill (including baseline comparisons) to measure impact
- Provides a browser-based eval viewer for qualitative review of outputs side-by-side across iterations
- Runs quantitative benchmarks with assertion grading, timing data, and variance analysis
- Optimizes skill descriptions for better triggering accuracy using an automated train/test evaluation loop
- Packages finished skills into installable `.skill` files

## Installation

**Option 1: Install the `.skill` file**

If you have a packaged `.skill` file, install it with:

```bash
claude install-skill skill-creator.skill
```

**Option 2: Copy the folder**

Copy the `skill-creator/` directory into your skills folder:

```bash
cp -r skill-creator/ ~/.claude/skills/skill-creator/
```

## What's Included

```
skill-creator/
├── SKILL.md                        # Main skill instructions
├── LICENSE.txt                     # License
├── agents/
│   ├── grader.md                   # Subagent instructions for assertion grading
│   ├── comparator.md               # Subagent instructions for blind A/B comparison
│   └── analyzer.md                 # Subagent instructions for benchmark analysis
├── scripts/
│   ├── run_loop.py                 # Description optimization loop
│   ├── run_eval.py                 # Trigger evaluation runner
│   ├── improve_description.py      # Description improvement via Claude
│   ├── aggregate_benchmark.py      # Aggregates grading results into benchmark.json
│   ├── package_skill.py            # Packages a skill folder into a .skill file
│   ├── generate_report.py          # Report generation utilities
│   ├── quick_validate.py           # Quick skill validation checks
│   └── utils.py                    # Shared utility functions
├── eval-viewer/
│   ├── generate_review.py          # Generates the browser-based eval review UI
│   └── viewer.html                 # HTML template for the eval viewer
├── assets/
│   └── eval_review.html            # HTML template for trigger eval query review
└── references/
    └── schemas.md                  # JSON schemas for evals, grading, and benchmarks
```

## Example Prompts

- "I want to create a skill that helps write and format technical blog posts with proper code blocks, metadata, and SEO tags. Let's set up some test cases and iterate on it."
- "I have an existing skill for generating database migrations but the outputs are inconsistent. Can you help me benchmark it and improve the instructions?"

## Platform Compatibility

| Platform    | Support Level | Notes                                                                 |
|-------------|---------------|-----------------------------------------------------------------------|
| Claude Code | Full          | All features including subagent parallel runs and description optimization |
| Cowork      | Full          | Uses `--static` flag for eval viewer; feedback via downloaded JSON     |
| Claude.ai   | Partial       | No subagents or description optimization; runs test cases sequentially |

## Related Skills

- Skills that follow the [Agent Skills specification](https://agentskills.io/specification) can be created and tested using this skill.
