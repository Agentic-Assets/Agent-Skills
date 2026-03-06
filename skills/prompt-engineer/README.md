# Prompt Engineer

Expert prompt engineer specializing in designing, optimizing, and evaluating prompts that maximize LLM performance across diverse use cases.

## What This Skill Does

- Designs prompts for new LLM applications using proven patterns like zero-shot, few-shot, and chain-of-thought
- Optimizes existing prompts for better accuracy, consistency, and token efficiency
- Builds evaluation and testing frameworks with quantitative metrics to measure prompt quality
- Creates system prompts with personas, guardrails, and context management strategies
- Implements structured output schemas including JSON mode, function calling, and schema validation
- Guides prompt migration between different models and providers with systematic testing

## Installation

### Option 1: `.skill` file

Create a file called `prompt-engineer.skill` in your project root:

```
/skills/prompt-engineer
```

Then install the skill folder to the path referenced above.

### Option 2: Copy the folder

Copy the `skills/prompt-engineer` folder directly into your project:

```
your-project/
  skills/
    prompt-engineer/
      SKILL.md
      references/
```

## What's Included

```
skills/prompt-engineer/
  SKILL.md
  references/
    evaluation-frameworks.md
    prompt-optimization.md
    prompt-patterns.md
    structured-outputs.md
    system-prompts.md
```

## Example Prompts

**Designing a classification prompt with structured output:**

> I need to build a prompt that classifies customer support tickets into categories (billing, technical, account, general) and returns structured JSON with the category, confidence score, and suggested routing. Help me design, test, and optimize this prompt.

**Debugging inconsistent LLM responses:**

> My summarization prompt works well on short articles but produces inconsistent results on longer documents. Sometimes it misses key points or hallucinates details. Help me diagnose the issue and iterate toward a more reliable prompt.

## Platform Compatibility

| Platform       | Supported |
|----------------|-----------|
| Claude Code    | Yes       |
| Cursor         | Yes       |
| Windsurf       | Yes       |
| Cline          | Yes       |
| Other AI IDEs  | Yes       |

## Related Skills

- **LLM Architect** - System design with LLM components
- **AI Engineer** - Production AI application development
- **Test Master** - Evaluation framework implementation
- **Technical Writer** - Prompt documentation and guidelines
