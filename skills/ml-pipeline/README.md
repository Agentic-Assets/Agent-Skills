# ML Pipeline

Production-grade machine learning infrastructure, orchestration systems, and automated training workflows.

## What This Skill Does

- **Feature Engineering**: Scikit-learn pipelines, feature stores (Feast), data validation
- **Training**: Distributed training, PyTorch/TensorFlow, checkpointing
- **Experiment Tracking**: MLflow, Weights & Biases, model registries
- **Hyperparameter Tuning**: Optuna, grid/random search, Bayesian optimization
- **Pipeline Orchestration**: Kubeflow, Airflow, Prefect DAGs
- **Deployment**: Model validation, A/B testing, shadow deployment, canary releases

## Installation

### Option 1: Download the `.skill` file (Easiest)

Download `ml-pipeline.skill` from this directory and place it in your skills folder:

```bash
cp ml-pipeline.skill ~/.claude/skills/
```

### Option 2: Copy the skill folder

```bash
cp -r skills/ml-pipeline ~/.claude/skills/
```

## What's Included

```
ml-pipeline/
├── SKILL.md                              # Core skill with quick-start patterns
├── references/
│   ├── feature-engineering.md            # Feature pipelines, stores, validation
│   ├── training-pipelines.md             # Distributed training, hyperopt, GPUs
│   ├── experiment-tracking.md            # MLflow, W&B, model registry
│   ├── pipeline-orchestration.md         # Kubeflow, Airflow, Prefect DAGs
│   └── model-validation.md              # Evaluation, A/B testing, shadow deploy
```

## Example Prompts

```
Build an end-to-end ML pipeline for customer churn prediction.
Use scikit-learn for preprocessing, XGBoost for training,
MLflow for experiment tracking, and Optuna for hyperparameter tuning.
```

```
Set up a Kubeflow pipeline that runs daily: validate incoming data
with Great Expectations, compute features, train the model,
evaluate against the production model, and deploy if metrics improve.
```

## Platform Compatibility

| Platform | Status | Notes |
|----------|--------|-------|
| Claude Code | Full support | Copy to `~/.claude/skills/` |
| Claude.ai | Full support | Upload SKILL.md as project knowledge |
| Other LLM platforms | Full | Use SKILL.md content as system prompt |

## Related Skills

- **pandas-pro** - DataFrame manipulation for feature engineering
- **matplotlib** / **scientific-visualization** - Model performance visualization
