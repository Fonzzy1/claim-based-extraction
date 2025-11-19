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
    [+] Building 0.0s (0/1)                                                         
     => [internal] load local bake definitions                                 0.0s
    [+] Building 0.2s (2/3)                                                         
     => [internal] load local bake definitions                                 0.0s
     => => reading from stdin 537B                                             0.0s
     => [internal] load build definition from Dockerfile                       0.0s
     => => transferring dockerfile: 423B                                       0.0s
     => [internal] load metadata for docker.io/library/python:3.10             0.2s
    [+] Building 0.3s (3/3)                                                         
     => [internal] load local bake definitions                                 0.0s
     => => reading from stdin 537B                                             0.0s
     => [internal] load build definition from Dockerfile                       0.0s
     => => transferring dockerfile: 423B                                       0.0s
     => [internal] load metadata for docker.io/library/python:3.10             0.3s
    [+] Building 0.4s (16/16) FINISHED                                              
     => [internal] load local bake definitions                                 0.0s
     => => reading from stdin 537B                                             0.0s
     => [internal] load build definition from Dockerfile                       0.0s
     => => transferring dockerfile: 423B                                       0.0s
     => [internal] load metadata for docker.io/library/python:3.10             0.3s
     => [internal] load .dockerignore                                          0.0s
     => => transferring context: 2B                                            0.0s
     => [internal] load build context                                          0.0s
     => => transferring context: 3.05kB                                        0.0s
     => [1/9] FROM docker.io/library/python:3.10@sha256:8b08e9b7203aec1d22b78  0.0s
     => CACHED [2/9] WORKDIR /app                                              0.0s
     => CACHED [3/9] COPY requirements.txt requirements.txt                    0.0s
     => CACHED [4/9] RUN pip install --no-cache-dir -r requirements.txt        0.0s
     => CACHED [5/9] COPY ./db ./db                                            0.0s
     => CACHED [6/9] RUN  prisma generate --schema ./db/schema.prisma          0.0s
     => CACHED [7/9] RUN python -m nltk.downloader punkt_tab                   0.0s
     => CACHED [8/9] COPY ./models ./models                                    0.0s
     => CACHED [9/9] COPY ./pipeline.py ./pipeline.py                          0.0s
     => exporting to image                                                     0.0s
     => => exporting layers                                                    0.0s
     => => writing image sha256:072b81ca8eab21433d2334a09839c286d9fe376a7d91b  0.0s
     => => naming to docker.io/library/claim-based-extraction-pipeline         0.0s
     => resolving provenance for metadata file                                 0.0s
    [+] Building 1/1
     ✔ claim-based-extraction-pipeline  B...                                   0.0s 
    [+] Running 0/1
     ⠋ ollama Pulling                                                          0.1s 
    [+] Running 0/1
     ⠙ ollama Pulling                                                          0.2s 
    [+] Running 0/1
     ⠹ ollama Pulling                                                          0.3s 
    [+] Running 0/1
     ⠸ ollama Pulling                                                          0.4s 
    [+] Running 0/1
     ⠼ ollama Pulling                                                          0.5s 
    [+] Running 0/1
     ⠴ ollama Pulling                                                          0.6s 
    [+] Running 0/1
     ⠦ ollama Pulling                                                          0.7s 
    [+] Running 0/1
     ⠧ ollama Pulling                                                          0.8s 
    [+] Running 0/1
     ⠇ ollama Pulling                                                          0.9s 
    [+] Running 0/1
     ⠏ ollama Pulling                                                          1.0s 
    [+] Running 0/1
     ⠋ ollama Pulling                                                          1.1s 
    [+] Running 0/1
     ⠙ ollama Pulling                                                          1.2s 
    [+] Running 0/1
     ⠹ ollama Pulling                                                          1.3s 
    [+] Running 0/1
     ⠸ ollama Pulling                                                          1.4s 
    [+] Running 0/1
     ⠼ ollama Pulling                                                          1.5s 
    [+] Running 0/1
     ⠴ ollama Pulling                                                          1.6s 
    [+] Running 0/1
     ⠦ ollama Pulling                                                          1.7s 
    [+] Running 0/1
     ⠧ ollama Pulling                                                          1.8s 
    [+] Running 0/1
     ⠇ ollama Pulling                                                          1.9s 
    [+] Running 0/1
     ⠏ ollama Pulling                                                          2.0s 
    [+] Running 1/1
     ✔ ollama Pulled                                                           2.1s 
    WARN[0002] Found orphan containers ([claim-based-extraction-pipeline-run-329508f9d237 claim-based-extraction-pipeline-run-22b06ecc192d claim-based-extraction-pipeline-run-1f5021321460 claim-based-extraction-pipeline-run-508fad2ae74b claim-based-extraction-pipeline-run-5a5c20fb8a8f claim-based-extraction-pipeline-run-328549ebdaf9 claim-based-extraction-pipeline-run-76a4f0ea1d54 claim-based-extraction-pipeline-run-686cb5d13ea9 claim-based-extraction-pipeline-run-c33ad085449a claim-based-extraction-pipeline-run-776330fa825e claim-based-extraction-pipeline-run-b7fed994a9c6 claim-based-extraction-pipeline-run-af3118b62155 claim-based-extraction-pipeline-run-bd908f402de8 claim-based-extraction-pipeline-run-33e06cfb46e8 claim-based-extraction-pipeline-run-65cad7459858 claim-based-extraction-pipeline-run-2c211f08d032 claim-based-extraction-pipeline-run-8902924c477e claim-based-extraction-pipeline-run-b37505dc12bf claim-based-extraction-pipeline-run-6d5becb8dd31 claim-based-extraction-pipeline-run-187704335e7f claim-based-extraction-pipeline-run-d86440976940 claim-based-extraction-pipeline-run-0662189a49c6 claim-based-extraction-pipeline-run-aad8c8444c14 claim-based-extraction-pipeline-run-7ba048b30c9d claim-based-extraction-pipeline-run-288efd5d7c61 claim-based-extraction-pipeline-run-0fd1b47ed638 claim-based-extraction-pipeline-run-94db7d74da28 claim-based-extraction-pipeline-run-0abc9c4b2b0d claim-based-extraction-pipeline-run-369e559c6d1c]) for this project. If you removed or renamed this service in your compose file, you can run this command with the --remove-orphans flag to clean it up. 
    [+] Running 3/4
     ✔ Container claim-based-extraction-web-1       Running                    0.0s 
     ✔ Container federal-hansard-db                 Running                    0.0s 
     ✔ Container claim-based-extraction-ollama-1    Running                    0.0s 
     ⠋ Container claim-based-extraction-pipeline-1  Starting                   0.0s 
    [+] Running 4/4
     ✔ Container claim-based-extraction-web-1       Running                    0.0s 
     ✔ Container federal-hansard-db                 Running                    0.0s 
     ✔ Container claim-based-extraction-ollama-1    Running                    0.0s 
     ✔ Container claim-based-extraction-pipeline-1  Started                    0.1s 
    ✅ Database already filled
    experiments/configs/2025-11-17-FILTERTEST-simple.yml
    experiments/configs/2025-11-19-FILTERTEST-add-techs-l2-and-orgs-and-sites-v2.yml
    experiments/configs/2025-11-19-FILTERTEST-add-techs-l2-and-orgs-and-sites.yml
    experiments/configs/2025-11-19-FILTERTEST-add-techs-l2-and-orgs.yml
    experiments/configs/2025-11-19-FILTERTEST-add-techs-l2.yml
    experiments/configs/2025-11-19-FILTERTEST-add-techs.yml
    experiments/configs/2025-11-19-FILTERTEST-e-or-p.yml

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
    False    973
    True      27
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
df_metrics = pd.DataFrame(metric_table).sort_values(by='F1')
```

    /tmp/ipykernel_100154/2248653284.py:26: FutureWarning:

    Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version. Call result.infer_objects(copy=False) instead. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`

    /tmp/ipykernel_100154/2248653284.py:26: FutureWarning:

    Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version. Call result.infer_objects(copy=False) instead. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`

    /tmp/ipykernel_100154/2248653284.py:26: FutureWarning:

    Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version. Call result.infer_objects(copy=False) instead. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`

    /tmp/ipykernel_100154/2248653284.py:26: FutureWarning:

    Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version. Call result.infer_objects(copy=False) instead. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`

    /tmp/ipykernel_100154/2248653284.py:26: FutureWarning:

    Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version. Call result.infer_objects(copy=False) instead. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`

    /tmp/ipykernel_100154/2248653284.py:26: FutureWarning:

    Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version. Call result.infer_objects(copy=False) instead. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`

    /tmp/ipykernel_100154/2248653284.py:26: FutureWarning:

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
execution_count="7">

|  |  | accuracy | precision | recall | f1 |
|----|----|---:|---:|---:|---:|
| 6 | experiments/configs/2025-11-19-FILTERTEST-e-or-p.yml | 0.977 | 0.75 | 0.222222 | 0.342857 |
| 3 | experiments/configs/2025-11-17-FILTERTEST-simple.yml | 0.979 | 1 | 0.222222 | 0.363636 |
| 1 | experiments/configs/2025-11-19-FILTERTEST-add-techs.yml | 0.977 | 0.7 | 0.259259 | 0.378378 |
| 2 | experiments/configs/2025-11-19-FILTERTEST-add-techs-l2-and-orgs-and-sites.yml | 0.989 | 0.710526 | 1 | 0.830769 |
| 4 | experiments/configs/2025-11-19-FILTERTEST-add-techs-l2.yml | 0.99 | 0.742857 | 0.962963 | 0.83871 |
| 0 | experiments/configs/2025-11-19-FILTERTEST-add-techs-l2-and-orgs-and-sites-v2.yml | 0.99 | 0.72973 | 1 | 0.84375 |
| 5 | experiments/configs/2025-11-19-FILTERTEST-add-techs-l2-and-orgs.yml | 0.99 | 0.72973 | 1 | 0.84375 |

</div>

</div>

``` python
# 1. Best filter with highest F1
best_row = df_metrics.loc[df_metrics['F1'].idxmax()]
best_config = best_row['config']
best_result_path = best_config.replace('configs', 'results').replace('.yml',
'.pkl')

# 2. Prepare prediction/gold comparison
trial_corpus = Corpus.load_from_file(best_result_path)
df_pred = pd.DataFrame([{'id': doc.id} for doc in trial_corpus.documents])
if df_pred.empty:
    df_pred = pd.DataFrame(columns=['id'])
df_pred['filter_pred'] = True

df_comp = pd.merge(df, df_pred[['id', 'filter_pred']], on='id', how='left')
df_comp['filter_pred'] = df_comp['filter_pred'].fillna(False)

# 3. Find errors
df_wrong = df_comp[df_comp['filter'] != df_comp['filter_pred']]

from tabulate import tabulate

Markdown(tabulate(df_wrong[['id', 'title', 'filter', 'filter_pred']], headers="keys"))
```

    /tmp/ipykernel_100154/1775018809.py:15: FutureWarning:

    Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version. Call result.infer_objects(copy=False) instead. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`

|  | id | title | filter | filter_pred |
|----|---:|:---|:---|:---|
| 177 | 1814726 | BILLS, Security of Critical Infrastructure Bill 2017, Security of Critical Infrastructure (Consequential and Transitional Provisions) Bill 2017, First Reading | False | True |
| 225 | 1570654 | MATTERS OF PUBLIC IMPORTANCE, Mining and Taxation Policies | False | True |
| 241 | 1256676 | JABILUKA URANIUM MINE, COMMITTEES, Privileges Committee, Report | False | True |
| 368 | 1561241 | CONSTITUENCY STATEMENTS, Windale Community Information and Assistance Expo | False | True |
| 437 | 2206504 | ANSWERS TO QUESTIONS UPON NOTICE, Petrol: Lead Content (Question No. 1544) | False | True |
| 522 | 1668043 | BILLS, Security Legislation Amendment (Critical Infrastructure) Bill 2020, Third Reading | False | True |
| 524 | 1909459 | ANSWERS TO QUESTIONS UPON NOTICE, Transmission Equipment (Question 1249) | False | True |
| 649 | 1479071 | QUESTIONS WITHOUT NOTICE, MINING AT KANMANTOO | False | True |
| 682 | 1641466 | STATEMENTS BY MEMBERS, Beagley, Archdeacon William ‘Bill’ Alan | False | True |
| 724 | 1525333 | QUESTIONS IN WRITING, Human Services: Electricity and Water | False | True |
