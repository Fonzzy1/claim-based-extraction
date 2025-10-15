# claim-based-extraction

claim-analysis/
├── README.md # Project overview and setup
├── requirements.txt # Python dependencies
├── .gitignore # Ignore data, checkpoints, outputs, etc.
├── Makefile # (Optional) run pipeline, setup, render analysis
│
├── db/ # 🔗 Submodule: raw speeches database
│ └── speeches.sqlite # SQLite DB with raw speech text
│
├── data/ # 💾 All pipeline outputs and annotations
│ ├── interim/ # Extracted claims, intermediate outputs
│ ├── processed/ # Final triplets ready for analysis
│ └── annotations/ # Gold data for claim & triplet labeling
│
├── models/ # 🧠 Model wrappers and training code
│ ├── base.py # Optional base class for models
│ ├── claim_extraction/
│ │ ├── train.py
│ │ ├── infer.py
│ │ └── utils.py
│ ├── triplet_extraction/
│ │ ├── train.py
│ │ ├── infer.py
│ │ └── utils.py
│ └── model_utils.py # Shared model loading/checkpointing
│
├── pipelines/ # 🔁 End-to-end orchestration scripts
│ ├── run_pipeline.py # Full pipeline: DB → claims → triplets
│ ├── claim_pipeline.py # Just claim extraction
│ ├── triplet_pipeline.py # Just triplet generation
│ └── eval_pipeline.py # Evaluation scripts
│
├── utils/ # 🔧 Helper modules
│ ├── db_loader.py # Load speech from SQLite DB
│ ├── preprocess.py # Text cleaning, paragraph segmentation
│ ├── labeling.py # Labeling templates, JSON I/O
│ └── logging_config.py # Central logging setup
│
├── experiments/ # ⚗️ Experiment configs & results
│ ├── configs/
│ │ ├── claim_extractor_t5.yaml
│ │ └── triplet_extractor_t5.yaml
│ └── results/
│ └── exp_001/
│ ├── logs.txt
│ └── triplets_output.json
│
├── analysis/ # 📊 Quarto notebooks + scripts
│ ├── notebooks/
│ │ ├── claim_summary.qmd
│ │ ├── triplet_patterns.qmd
│ │ └── error_analysis.qmd
│ └── scripts/
│ └── analyze_triplets.py # Structured CLI/script analysis
│
├── tests/ # ✅ Unit tests
│ ├── test_db_loader.py
│ ├── test_claim_pipeline.py
│ └── test_triplet_pipeline.py
