# Claim Based Extraction

This repository implements an end-to-end pipeline for **claim extraction and triplet generation** from speech transcripts, including model training, inference, and experiment management.

---

## 📁 Project Structure

```
claim-analysis/
├── README.md               # Project overview and setup
├── requirements.txt        # Python dependencies
├── docker-compose.yml      # Compose file for CPU based work
├── docker-compose-gpu.yml  # Compose file for GPU based work
├── Dockerfile              # Docker file for experiment runner
├── run.sh                  # Autodetector for upping background utilities
├── .gitignore              # Ignore data, outputs, checkpoints
│
├── db/                     # Submodule: https://github.com/Fonzzy1/federal-hansard-db
├── data/                   # Pipeline data
│   ├── clean.py            # Script for preparing raw texts
│   ├── annotator.py        # Script for adding Gold Standard Labels
│   └── annotations/        # Gold-standard labels (small files, versioned)
│       ├── train/          # Training set (80% of labels)
│       └── test/           # Test set (20% of labels)
│
├── models/                 # Reusable ML code
│   ├── filter/             # Classes for filter
│   ├── extraction/         # Classes for extraction models
│   ├── deconstruction/     # Classes for deconstruction models
│   └── base_model.py       # Universal model for all of the classes
│
├── pipelines/              # Orchestrator scripts
│   ├── filter/             # Train / inferance for filter
│   ├── extraction/         # Train / inferance for extraction
│   ├── deconstruction/     # Train / inferance for deconstruction
│   └── run_pipeline.py     # Full inference across the dataset with eval
│
├── experiments/            # Training & analysis experiments
│   ├── configs/            # YAML configs for reproducibility
│   └── results/            # Each experiment gets a unique folder
│
├── analysis/               # Notebooks and scripts for inspection/visualization
│
└── dashboard/              # Additional GUI browsing tool
```

---

## Key Principles

### 1. Models

- `models/` contains **reusable library code**.
- Training scripts can be run via CLI, but pipelines import model classes/functions.
- Model weights are considered **generated artifacts**, not versioned in Git.

### 2. Pipelines

- Scripts in `pipelines/` orchestrate the workflow: claim extraction → triplet generation → evaluation.
- Can be run end-to-end (`run_pipeline.py`) or in modular steps (`claim_pipeline.py`, `triplet_pipeline.py`).

### 3. Experiments

- Each training run or analysis is an **experiment**.
- Store **config files** in `experiments/configs/`.
- Store **outputs** (logs, triplets, checkpoints) in `experiments/results/exp_XXX/`.
- Never overwrite results; each run gets a unique folder.

### 4. Data Management

- **Version small, immutable data** (annotations) in Git.
- **Raw or large data** should be stored externally (e.g., S3, GDrive, SQLite DB outside repo).
- Pipeline outputs (`interim/`, `processed/`) and model checkpoints should be **ignored by Git**.

### 5. Reproducibility

- Experiments + configs ensure **training runs are reproducible**.
- Pipelines + model code + utils should be **importable and modular**.
- Optional: Docker can encapsulate the environment for full reproducibility.

---

## ⚙️ Optional Docker Setup

- **Single Dockerfile** at project root is sufficient.
- Mount external volumes for `data/` and `experiments/results/` to persist outputs.
- Pipelines can be run inside the container with:

```bash
docker build -t claim-analysis:latest .
docker run -it --rm -v $(pwd)/data:/app/data -v $(pwd)/experiments/results:/app/experiments/results claim-analysis:latest
```

- For GPU-based model training, use a `pytorch/pytorch:latest` base image.

---

## 🛠 Recommended Workflow

1. Add gold-standard labels to `data/annotations/`.
2. Prepare experiment config in `experiments/configs/`.
3. Run pipelines to train models or generate triplets.
4. Store logs, outputs, and checkpoints in a **unique experiment folder**.
5. Analyze results in `analysis/` notebooks or scripts.

---

## 📊 Dashboard and HTML Analysis

For interactive analysis and HTML browsing, a dashboard can be generated using Python tools such as **Plotly Dash** or **Panel**. Recommended setup:

1. Install dashboard dependencies in `requirements.txt`:

```bash
pip install dash plotly panel
```

2. Example dashboard script (`analysis/scripts/dashboard.py`):

```python
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html

# Load processed triplets
df = pd.read_json('../../experiments/results/exp_001/triplets_output.json')

app = Dash(__name__)

app.layout = html.Div([
    html.H1('Claim Analysis Dashboard'),
    dcc.Graph(
        figure=px.bar(df, x='claim_type', y='count', color='category', title='Claim Distribution')
    )
])

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)
```

3. Run the dashboard locally or inside Docker, then browse at `http://localhost:8050`.
4. Customize graphs, filters, and interactive elements for deeper analysis.

This allows **quick visual inspection of claims, triplet patterns, and experiment results** directly in a browser, improving reproducibility and collaboration.
