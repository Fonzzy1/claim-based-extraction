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

