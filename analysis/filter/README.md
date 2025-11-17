# Filter Testing


``` python
import os
os.chdir('../../')
! bash ./analysis/filter/generate_filter_results.sh
```

    Checking for client.json...
    ✅ client.json exists
    🔄 Updating git submodules...
    fatal: detected dubious ownership in repository at '/claim-based-extraction/db'
    To add an exception for this directory, call:

        git config --global --add safe.directory /claim-based-extraction/db
    fatal: Unable to find current revision in submodule path 'db'
    🚀 Running auto 'up'...
    WARN[0000] Found orphan containers ([claim-based-extraction-pipeline-run-dbbd5f76dfd3 claim-based-extraction-pipeline-run-238cce378f38 claim-based-extraction-pipeline-run-c18d5baee712 claim-based-extraction-pipeline-run-57aaa9d3c84f claim-based-extraction-pipeline-run-ad9fc13e8f64 claim-based-extraction-pipeline-run-3f802f0548a8 claim-based-extraction-pipeline-run-2b8fbc534e58 claim-based-extraction-pipeline-run-a18479a91a34 claim-based-extraction-pipeline-run-befe9f1b5180 claim-based-extraction-pipeline-run-6ca70a0893b6 claim-based-extraction-pipeline-run-fab116e9326c claim-based-extraction-pipeline-run-393cf094a24f claim-based-extraction-pipeline-run-e20237cbe222 claim-based-extraction-pipeline-run-ce964814c62d claim-based-extraction-pipeline-run-9d0628f9cc04 claim-based-extraction-pipeline-run-7ba37ec18833 claim-based-extraction-pipeline-run-e49782ec80cb claim-based-extraction-pipeline-run-6b5aa8877051 claim-based-extraction-pipeline-run-9cc693a7fa77 claim-based-extraction-pipeline-run-f5a0aaa8095e claim-based-extraction-pipeline-run-797e466275ca claim-based-extraction-download-run-4b7ed895a996 claim-based-extraction-download-run-38f17f649a05]) for this project. If you removed or renamed this service in your compose file, you can run this command with the --remove-orphans flag to clean it up. 
    [+] Running 2/3
     ✔ Container federal-hansard-db                 Running                    0.0s 
     ✔ Container claim-based-extraction-web-1       Running                    0.0s 
     ⠋ Container claim-based-extraction-pipeline-1  Starting                   0.1s 
    [+] Running 3/3
     ✔ Container federal-hansard-db                 Running                    0.0s 
     ✔ Container claim-based-extraction-web-1       Running                    0.0s 
     ✔ Container claim-based-extraction-pipeline-1  Started                    0.1s 
    ✅ Database already filled
    experiments/configs/2025-11-17-FILTERTEST-simple.yml
    WARN[0000] Found orphan containers ([claim-based-extraction-pipeline-run-dbbd5f76dfd3 claim-based-extraction-pipeline-run-238cce378f38 claim-based-extraction-pipeline-run-c18d5baee712 claim-based-extraction-pipeline-run-57aaa9d3c84f claim-based-extraction-pipeline-run-ad9fc13e8f64 claim-based-extraction-pipeline-run-3f802f0548a8 claim-based-extraction-pipeline-run-2b8fbc534e58 claim-based-extraction-pipeline-run-a18479a91a34 claim-based-extraction-pipeline-run-befe9f1b5180 claim-based-extraction-pipeline-run-6ca70a0893b6 claim-based-extraction-pipeline-run-fab116e9326c claim-based-extraction-pipeline-run-393cf094a24f claim-based-extraction-pipeline-run-e20237cbe222 claim-based-extraction-pipeline-run-ce964814c62d claim-based-extraction-pipeline-run-9d0628f9cc04 claim-based-extraction-pipeline-run-7ba37ec18833 claim-based-extraction-pipeline-run-e49782ec80cb claim-based-extraction-pipeline-run-6b5aa8877051 claim-based-extraction-pipeline-run-9cc693a7fa77 claim-based-extraction-pipeline-run-f5a0aaa8095e claim-based-extraction-pipeline-run-797e466275ca claim-based-extraction-download-run-4b7ed895a996 claim-based-extraction-download-run-38f17f649a05]) for this project. If you removed or renamed this service in your compose file, you can run this command with the --remove-orphans flag to clean it up. 
    /usr/local/lib/python3.10/site-packages/google/api_core/_python_version_support.py:266: FutureWarning: You are using a Python version (3.10.19) which Google will stop supporting in new releases of google.api_core once it reaches its end of life (2026-10-04). Please upgrade to the latest Python version, or at least Python 3.11, to continue receiving updates for google.api_core past that date.
      warnings.warn(message, FutureWarning)
    Loading Config ...
    Pulling Data
    Loading Filter ...
    Filtering Documents ...
      0%|                                                  | 0/1000 [00:00<?, ?it/s]100%|███████████████████████████████████| 1000/1000 [00:00<00:00, 312355.08it/s]

``` python
from models.base_model import Corpus 
import pandas as pd

labeled_corpus = Corpus.load_from_file('data/labeled/filter/labeled_examples.pkl')
df = pd.DataFrame([{'title': doc.title, 'text': doc.text, 'filter': doc.filter, 'id': doc.id} for doc in labeled_corpus.documents])

df.info()
df['filter'].value_counts()
```

    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 1000 entries, 0 to 999
    Data columns (total 4 columns):
     #   Column  Non-Null Count  Dtype 
    ---  ------  --------------  ----- 
     0   title   1000 non-null   object
     1   text    1000 non-null   object
     2   filter  1000 non-null   bool  
     3   id      1000 non-null   int64 
    dtypes: bool(1), int64(1), object(2)
    memory usage: 24.5+ KB

    filter
    False    977
    True      23
    Name: count, dtype: int64

``` python
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import glob
filters = glob.glob('experiments/configs/*FILTERTEST*')
results = [path.replace('configs', 'results').replace('.yml', '.pkl') for path in filters]
zipped = list(zip(filters, results))

# Load gold standard
# Get config/result pairs
filters = glob.glob('experiments/configs/*FILTERTEST*')
results = [path.replace('configs', 'results').replace('.yml', '.pkl') for path
in filters]
zipped = list(zip(filters, results))
metric_table = []
for config, result_path in zipped:
    trial_corpus = Corpus.load_from_file(result_path)
    df_pred = pd.DataFrame([{'id': doc.id} for doc in trial_corpus.documents])
    # If nothing passed the filter, create empty DataFrame with right columns
    if df_pred.empty:
        df_pred = pd.DataFrame(columns=['id'])
    df_pred['filter_pred'] = True  # All returned docs were kept
    
    # Merge with gold data (left join to keep all gold)
    df_comp = pd.merge(df, df_pred[['id', 'filter_pred']], on='id', how='left')
    # 'filter_pred' will be NaN for those not caught by filter, i.e. predicted
    # False
    df_comp['filter_pred'] = df_comp['filter_pred'].fillna(False)

    y_true = df_comp['filter']
    y_pred = df_comp['filter_pred']

    acc = accuracy_score(y_true, y_pred)
    prec = precision_score(y_true, y_pred, average='binary', zero_division=0)
    rec = recall_score(y_true, y_pred, average='binary', zero_division=0)
    f1 = f1_score(y_true, y_pred, average='binary', zero_division=0)

    metric_table.append({
        'config': config,
        'Accuracy': acc,
        'Precision': prec,
        'Recall': rec,
        'F1': f1
    })
df_metrics = pd.DataFrame(metric_table)
```

    /tmp/ipykernel_10531/1267431509.py:26: FutureWarning:

    Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version. Call result.infer_objects(copy=False) instead. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`

``` python
from IPython.display import Markdown
from tabulate import tabulate

Markdown(tabulate(df_metrics, headers=["accuracy", "precision", "recall",
"f1"]))
```

<div id="tbl-planet-measures">

Table 1: Astronomical object

<div class="cell-output cell-output-display cell-output-markdown"
execution_count="16">

|  |  | accuracy | precision | recall | f1 |
|----|----|---:|---:|---:|---:|
| 0 | experiments/configs/2025-11-17-FILTERTEST-simple.yml | 0.977 | 0 | 0 | 0 |

</div>

</div>
