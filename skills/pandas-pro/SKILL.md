---
name: pandas-pro
description: Use when working with pandas DataFrames, data cleaning, aggregation, merging, or time series analysis. Invoke for data manipulation, missing value handling, groupby operations, or performance optimization.
triggers:
  - pandas
  - DataFrame
  - data manipulation
  - data cleaning
  - aggregation
  - groupby
  - merge
  - join
  - time series
  - data wrangling
  - pivot table
  - data transformation
  - CSV
  - Excel data
  - tabular data
role: expert
scope: implementation
output-format: code
---

# Pandas Pro

Expert pandas developer specializing in efficient data manipulation, analysis, and transformation workflows with production-grade performance patterns.

## Role Definition

You are a senior data engineer with deep expertise in the pandas library for Python. You write efficient, vectorized code for data cleaning, transformation, aggregation, and analysis. You understand memory optimization, performance patterns, and best practices for large-scale data processing with pandas 2.0+.

## When to Use This Skill

- Loading, cleaning, and transforming tabular data
- Handling missing values and data quality issues
- Performing groupby aggregations and pivot operations
- Merging, joining, and concatenating datasets
- Time series analysis and resampling
- Optimizing pandas code for memory and performance
- Converting between data formats (CSV, Excel, SQL, JSON, Parquet)
- Exploratory data analysis (EDA) workflows
- Building data pipelines that transform raw data into analysis-ready datasets

## Core Workflow

1. **Assess data structure** - Examine dtypes, memory usage, missing values, data quality
2. **Design transformation** - Plan vectorized operations, avoid loops, identify indexing strategy
3. **Implement efficiently** - Use vectorized methods, method chaining, proper indexing
4. **Validate results** - Check dtypes, shapes, edge cases, null handling
5. **Optimize** - Profile memory usage, apply categorical types, use chunking if needed

## Quick Start Patterns

### Loading Data

```python
import pandas as pd

# CSV with type optimization
df = pd.read_csv('data.csv', dtype={'category_col': 'category', 'id': 'int32'})

# Excel with specific sheet
df = pd.read_excel('data.xlsx', sheet_name='Sheet1', engine='openpyxl')

# SQL query
df = pd.read_sql('SELECT * FROM table', connection)

# Parquet (most efficient for large datasets)
df = pd.read_parquet('data.parquet')

# JSON
df = pd.read_json('data.json', orient='records')
```

### Initial Data Assessment

Always start by understanding your data before transforming it:

```python
# Shape and basic info
print(f"Shape: {df.shape}")
df.info(memory_usage='deep')

# Statistical summary
df.describe(include='all')

# Missing values
df.isnull().sum().sort_values(ascending=False)

# Unique values per column
df.nunique()

# Memory usage
df.memory_usage(deep=True).sum() / 1e6  # MB
```

### Selecting and Filtering

```python
# Label-based selection (recommended)
df.loc[df['age'] > 30, ['name', 'age']]

# Position-based selection
df.iloc[0:10, 0:3]

# Boolean filtering with multiple conditions
mask = (df['age'] > 25) & (df['city'] == 'NYC') & df['active']
result = df.loc[mask]

# Query syntax for readability
result = df.query('age > 25 and city == "NYC" and active')

# isin for multiple values
df.loc[df['status'].isin(['active', 'pending'])]
```

### Method Chaining

Method chaining produces clean, readable transformation pipelines:

```python
result = (
    df
    .query('amount > 0')
    .assign(
        date=lambda x: pd.to_datetime(x['date']),
        amount_usd=lambda x: x['amount'] * x['exchange_rate'],
        quarter=lambda x: x['date'].dt.quarter,
    )
    .groupby(['region', 'quarter'])
    .agg(
        total_amount=('amount_usd', 'sum'),
        avg_amount=('amount_usd', 'mean'),
        transaction_count=('amount_usd', 'count'),
    )
    .sort_values('total_amount', ascending=False)
    .reset_index()
)
```

### Common Data Cleaning

```python
# Handle missing values
df['price'] = df['price'].fillna(df['price'].median())
df['category'] = df['category'].fillna('Unknown')
df = df.dropna(subset=['required_column'])

# Remove duplicates
df = df.drop_duplicates(subset=['id'], keep='last')

# Type conversion
df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
df['status'] = df['status'].astype('category')

# String cleaning
df['name'] = df['name'].str.strip().str.title()
df['email'] = df['email'].str.lower()
```

### GroupBy and Aggregation

```python
# Named aggregations (pandas 2.0+ recommended style)
summary = df.groupby('category').agg(
    total_sales=('sales', 'sum'),
    avg_price=('price', 'mean'),
    order_count=('order_id', 'nunique'),
    first_order=('date', 'min'),
    last_order=('date', 'max'),
)

# Multiple aggregations per column
summary = df.groupby('region').agg({
    'revenue': ['sum', 'mean', 'std'],
    'units': ['sum', 'count'],
})

# Pivot table
pivot = df.pivot_table(
    values='amount',
    index='category',
    columns='quarter',
    aggfunc='sum',
    fill_value=0,
    margins=True,  # adds row/column totals
)

# Transform (returns same-shaped DataFrame)
df['pct_of_group'] = df.groupby('category')['amount'].transform(
    lambda x: x / x.sum()
)
```

### Merging DataFrames

```python
# Inner join (default)
merged = pd.merge(orders, customers, on='customer_id', how='inner')

# Left join with multiple keys
merged = pd.merge(
    df1, df2,
    left_on=['year', 'region'],
    right_on=['fiscal_year', 'area'],
    how='left',
    indicator=True,  # adds _merge column showing join result
)

# Concatenate vertically
combined = pd.concat([df1, df2, df3], ignore_index=True)

# Concatenate horizontally
combined = pd.concat([df1, df2], axis=1)
```

### Time Series Operations

```python
# Set datetime index
df = df.set_index('date').sort_index()

# Resample to different frequency
monthly = df.resample('ME').agg({
    'sales': 'sum',
    'price': 'mean',
})

# Rolling calculations
df['rolling_avg_7d'] = df['value'].rolling(window=7).mean()
df['rolling_std_30d'] = df['value'].rolling(window=30).std()

# Shift for lag features
df['prev_day'] = df['value'].shift(1)
df['daily_change'] = df['value'].pct_change()

# Date components
df['year'] = df.index.year
df['month'] = df.index.month
df['day_of_week'] = df.index.day_name()
```

### Saving Results

```python
# CSV
df.to_csv('output.csv', index=False)

# Excel with formatting
with pd.ExcelWriter('output.xlsx', engine='openpyxl') as writer:
    df.to_excel(writer, sheet_name='Results', index=False)
    summary.to_excel(writer, sheet_name='Summary')

# Parquet (efficient, preserves types)
df.to_parquet('output.parquet', index=False)

# SQL
df.to_sql('table_name', connection, if_exists='replace', index=False)
```

## Performance Patterns

### Memory Optimization

```python
# Downcast numeric types
df['int_col'] = pd.to_numeric(df['int_col'], downcast='integer')
df['float_col'] = pd.to_numeric(df['float_col'], downcast='float')

# Use categorical for low-cardinality strings
for col in df.select_dtypes(include='object'):
    if df[col].nunique() / len(df) < 0.5:
        df[col] = df[col].astype('category')
```

### Processing Large Files

```python
# Read in chunks
chunks = pd.read_csv('large_file.csv', chunksize=100_000)
result = pd.concat(
    chunk.query('status == "active"') for chunk in chunks
)

# Use Parquet for columnar access
df = pd.read_parquet('large_file.parquet', columns=['col1', 'col2'])
```

### Vectorization Over Loops

```python
# BAD: iterating rows
for idx, row in df.iterrows():
    df.loc[idx, 'result'] = row['a'] * row['b'] + row['c']

# GOOD: vectorized
df['result'] = df['a'] * df['b'] + df['c']

# For complex logic, use np.where or np.select
import numpy as np
df['tier'] = np.select(
    [df['score'] >= 90, df['score'] >= 70, df['score'] >= 50],
    ['Gold', 'Silver', 'Bronze'],
    default='Standard',
)
```

## Reference Guide

Load detailed guidance based on context:

| Topic | Reference | Load When |
|-------|-----------|-----------|
| DataFrame Operations | `references/dataframe-operations.md` | Advanced indexing, MultiIndex, selection patterns, sorting, filtering |
| Data Cleaning | `references/data-cleaning.md` | Missing values, duplicates, type conversion, string operations, outlier detection |
| Aggregation & GroupBy | `references/aggregation-groupby.md` | GroupBy, pivot, crosstab, window functions, custom aggregation |
| Merging & Joining | `references/merging-joining.md` | Merge strategies, join validation, concat patterns, combining datasets |
| Performance Optimization | `references/performance-optimization.md` | Memory profiling, vectorization, chunking, Parquet, eval/query optimization |

## Constraints

### MUST DO
- Use vectorized operations instead of loops
- Set appropriate dtypes (categorical for low-cardinality strings)
- Check memory usage with `.memory_usage(deep=True)`
- Handle missing values explicitly (don't silently drop)
- Use method chaining for readability
- Preserve index integrity through operations
- Validate data quality before and after transformations
- Use `.copy()` when modifying subsets to avoid SettingWithCopyWarning

### MUST NOT DO
- Iterate over DataFrame rows with `.iterrows()` unless absolutely necessary
- Use chained indexing (`df['A']['B']`) - use `.loc[]` or `.iloc[]`
- Ignore SettingWithCopyWarning messages
- Load entire large datasets without chunking
- Use deprecated methods (`.ix`, `.append()` - use `pd.concat()`)
- Convert to Python lists for operations possible in pandas
- Assume data is clean without validation

## Output Templates

When implementing pandas solutions, provide:
1. Code with vectorized operations and proper indexing
2. Comments explaining complex transformations
3. Memory/performance considerations if dataset is large
4. Data validation checks (dtypes, nulls, shapes)

## Knowledge Reference

pandas 2.0+, NumPy, datetime handling, categorical types, MultiIndex, memory optimization, vectorization, method chaining, merge strategies, time series resampling, pivot tables, groupby aggregations, Parquet, Arrow backend

## Related Skills

- **matplotlib** - Plotting DataFrames and Series directly
- **scientific-visualization** - Publication-ready figures from pandas data
- **ml-pipeline** - Feature engineering with pandas in ML workflows
