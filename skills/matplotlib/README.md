# Matplotlib

Expert-level matplotlib skill for creating static, animated, and interactive plots with fine-grained control over every visual element.

## What This Skill Does

- **Plot Types**: Line, scatter, bar, histogram, heatmap, contour, box, violin, 3D plots
- **Customization**: Colors, styles, annotations, legends, axis formatting
- **Multi-Panel Figures**: Subplots, GridSpec, mosaic layouts
- **Export**: PNG, PDF, SVG at publication-quality DPI
- **Best Practices**: Object-oriented API, colormap selection, accessibility

## Installation

### Option 1: Download the `.skill` file (Easiest)

Download `matplotlib.skill` from this directory and place it in your skills folder:

```bash
cp matplotlib.skill ~/.claude/skills/
```

### Option 2: Copy the skill folder

```bash
cp -r skills/matplotlib ~/.claude/skills/
```

## What's Included

```
matplotlib/
├── SKILL.md                      # Core skill (375 lines)
├── references/
│   ├── plot_types.md             # Complete catalog of plot types with examples
│   ├── styling_guide.md          # Colors, fonts, customization options
│   ├── api_reference.md          # Core classes and methods reference
│   └── common_issues.md          # Troubleshooting guide
└── scripts/
    ├── plot_template.py          # Template demonstrating plot types
    └── style_configurator.py     # Custom style sheet generator
```

## Example Prompts

```
Create a multi-panel figure with 4 subplots: a line chart of revenue over time,
a scatter plot of price vs. demand, a bar chart of sales by category,
and a heatmap of the correlation matrix.
```

```
Plot this time series data with a 30-day rolling average, confidence bands,
and annotations marking key events. Save as PDF at 300 DPI.
```

## Platform Compatibility

| Platform | Status | Notes |
|----------|--------|-------|
| Claude Code | Full support | Copy to `~/.claude/skills/` |
| Claude.ai | Full support | Upload SKILL.md as project knowledge |
| Other LLM platforms | Partial | Use SKILL.md content as system prompt |

## Related Skills

- **scientific-visualization** - Publication-ready figures for journal submission
- **pandas-pro** - Data manipulation before plotting
