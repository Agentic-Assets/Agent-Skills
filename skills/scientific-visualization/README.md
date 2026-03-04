# Scientific Visualization

Publication-ready scientific figures for journal submission with multi-panel layouts, significance annotations, error bars, and colorblind-safe palettes.

## What This Skill Does

- **Journal Figures**: Nature, Science, Cell, PLOS formatting standards
- **Multi-Panel Layouts**: GridSpec, panel labels, consistent styling
- **Statistical Rigor**: Error bars, significance markers, confidence intervals
- **Accessibility**: Colorblind-safe palettes (Okabe-Ito), grayscale compatibility
- **Export**: PDF, EPS, TIFF, PNG at journal-required DPI
- **Libraries**: matplotlib, seaborn, plotly integration

## Installation

### Option 1: Download the `.skill` file (Easiest)

Download `scientific-visualization.skill` from this directory and place it in your skills folder:

```bash
cp scientific-visualization.skill ~/.claude/skills/
```

### Option 2: Copy the skill folder

```bash
cp -r skills/scientific-visualization ~/.claude/skills/
```

## What's Included

```
scientific-visualization/
├── SKILL.md                          # Core skill (792 lines)
├── references/
│   ├── publication_guidelines.md     # Resolution, typography, layout rules
│   ├── color_palettes.md            # Colorblind-friendly palette specs
│   ├── journal_requirements.md       # Journal-specific technical specs
│   └── matplotlib_examples.md        # 10 complete working examples
├── scripts/
│   ├── figure_export.py             # Export utilities with journal presets
│   └── style_presets.py             # Pre-configured publication styles
└── assets/
    ├── color_palettes.py            # Importable color definitions
    ├── nature.mplstyle              # Nature journal matplotlib style
    ├── publication.mplstyle         # General publication style
    └── presentation.mplstyle        # Poster/slide style (larger fonts)
```

## Example Prompts

```
Create a 4-panel figure for Nature submission:
Panel A: bar chart comparing treatment groups with individual data points
Panel B: line plot with 95% CI showing time course
Panel C: correlation heatmap
Panel D: violin plot of distributions by condition
Use colorblind-safe colors and save as PDF.
```

```
I need to prepare Figure 3 for my Cell paper. It's a multi-panel figure
showing gene expression across 5 timepoints for 3 conditions.
Include error bars (SEM), significance annotations, and export at 300 DPI.
```

## Platform Compatibility

| Platform | Status | Notes |
|----------|--------|-------|
| Claude Code | Full support | Copy to `~/.claude/skills/` |
| Claude.ai | Full support | Upload SKILL.md as project knowledge |
| Other LLM platforms | Partial | Use SKILL.md content as system prompt; style files need manual setup |

## Related Skills

- **matplotlib** - Lower-level plot control and custom visualizations
- **pandas-pro** - Data preparation for visualization
