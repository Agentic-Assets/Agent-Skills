# Pandas Pro

Expert pandas developer for efficient data manipulation, analysis, and transformation with production-grade performance patterns.

## What This Skill Does

- **Data Loading**: CSV, Excel, SQL, JSON, Parquet with type optimization
- **Data Cleaning**: Missing values, duplicates, type conversion, string operations
- **Aggregation**: GroupBy, pivot tables, crosstab, window functions
- **Merging**: SQL-style joins, concatenation, combine strategies
- **Time Series**: Resampling, rolling calculations, lag features
- **Performance**: Memory optimization, vectorization, chunked processing

## Installation

### Option 1: Download the `.skill` file (Easiest)

Download `pandas-pro.skill` from this directory and place it in your skills folder:

```bash
cp pandas-pro.skill ~/.claude/skills/
```

### Option 2: Copy the skill folder

```bash
cp -r skills/pandas-pro ~/.claude/skills/
```

## What's Included

```
pandas-pro/
├── SKILL.md                              # Core skill with quick-start patterns
├── references/
│   ├── dataframe-operations.md           # Indexing, selection, filtering, sorting
│   ├── data-cleaning.md                  # Missing values, duplicates, type conversion
│   ├── aggregation-groupby.md            # GroupBy, pivot, crosstab, aggregation
│   ├── merging-joining.md                # Merge, join, concat strategies
│   └── performance-optimization.md       # Memory, vectorization, chunking
```

## Example Prompts

```
I have a CSV with 2M rows of sales data. Load it efficiently, clean missing
values in the price and category columns, then create a summary by region
and quarter showing total revenue, average order value, and customer count.
```

```
Merge these three DataFrames: orders (with customer_id), customers (with
demographics), and products (with categories). Then create a pivot table
showing average spend by age group and product category.
```

## Platform Compatibility

| Platform | Status | Notes |
|----------|--------|-------|
| Claude Code | Full support | Copy to `~/.claude/skills/` |
| Claude.ai | Full support | Upload SKILL.md as project knowledge |
| Other LLM platforms | Full | Use SKILL.md content as system prompt |

## Related Skills

- **matplotlib** - Plotting DataFrames and Series directly
- **scientific-visualization** - Publication-ready figures from pandas data
- **ml-pipeline** - Feature engineering with pandas in ML workflows
