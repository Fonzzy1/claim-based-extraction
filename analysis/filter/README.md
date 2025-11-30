# Filter Testing


``` python
import os
os.chdir('../../')
! bash ./analysis/filter/generate_filter_results.sh
```

    Checking for client.json...
    ✅ client.json exists
    🔄 Updating git submodules...
    Creating Docker volumes...
    [
        {
            "CreatedAt": "2025-11-20T14:36:23+11:00",
            "Driver": "local",
            "Labels": null,
            "Mountpoint": "/var/lib/docker/volumes/hansard_db_data/_data",
            "Name": "hansard_db_data",
            "Options": null,
            "Scope": "local"
        }
    ]
    [
        {
            "CreatedAt": "2024-12-16T21:50:44+11:00",
            "Driver": "local",
            "Labels": null,
            "Mountpoint": "/var/lib/docker/volumes/ollama/_data",
            "Name": "ollama",
            "Options": null,
            "Scope": "local"
        }
    ]
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
     => [1/9] FROM docker.io/library/python:3.10@sha256:20ca17b2908b0202fc975  0.0s
     => => resolve docker.io/library/python:3.10@sha256:20ca17b2908b0202fc975  0.0s
     => [internal] load build context                                          0.0s
     => => transferring context: 3.28kB                                        0.0s
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
     => => writing image sha256:11e766699215b1eb86cc64a37c88ff2d822afa6b77fde  0.0s
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
     ✔ ollama Pulled                                                           2.0s 
    WARN[0002] Found orphan containers ([claim-based-extraction-pipeline-run-ed1748583f85 claim-based-extraction-pipeline-run-9034a9d68212 claim-based-extraction-pipeline-run-9eb9b9aa38af claim-based-extraction-pipeline-run-eff65cbfc159 claim-based-extraction-pipeline-run-60bd1044355f claim-based-extraction-pipeline-run-f0db7aae1466 claim-based-extraction-db_manager-run-009107e55a24 claim-based-extraction-pipeline-run-75f23ce0f7da claim-based-extraction-pipeline-run-b042206b4340 claim-based-extraction-web-1]) for this project. If you removed or renamed this service in your compose file, you can run this command with the --remove-orphans flag to clean it up. 
    [+] Running 2/2
     ✔ Container ollama      Running                                           0.0s 
     ✔ Container hansard-db  Running                                           0.0s 
    ✅ Database already filled
    experiments/configs/2025-11-17-FILTERTEST-simple.yml
    experiments/configs/2025-11-19-FILTERTEST-add-techs-l2-and-orgs-and-sites-v2.yml
    experiments/configs/2025-11-19-FILTERTEST-add-techs-l2-and-orgs-and-sites.yml
    experiments/configs/2025-11-19-FILTERTEST-add-techs-l2-and-orgs.yml
    experiments/configs/2025-11-19-FILTERTEST-add-techs-l2.yml
    experiments/configs/2025-11-19-FILTERTEST-add-techs.yml
    experiments/configs/2025-11-19-FILTERTEST-e-or-p.yml
    experiments/configs/2025-11-20-FILTERTEST-vector-v1.yml
    experiments/configs/2025-11-20-FILTERTEST-vector-v2-lower-threshold.yml
    experiments/configs/2025-11-21-FILTERTEST-generative-v1.yml
    experiments/configs/2025-11-21-FILTERTEST-generative-v2.yml
    experiments/configs/2025-11-21-FILTERTEST-generative-v3-two-step.yml
    experiments/configs/2025-11-21-FILTERTEST-vector-v3-new-strings.yml
    experiments/configs/2025-11-21-FILTERTEST-vector-v4-rm_strings.yml
    experiments/configs/2025-11-21-FILTERTEST-vector-v5.yml
    experiments/configs/2025-11-21-FILTERTEST-vector-v6.yml
    experiments/configs/2025-11-21-FILTERTEST-vector-v7-5.yml
    experiments/configs/2025-11-21-FILTERTEST-vector-v7-6.yml
    experiments/configs/2025-11-21-FILTERTEST-vector-v7-7.yml
    experiments/configs/2025-11-21-FILTERTEST-vector-v7-8.yml
    experiments/configs/2025-11-21-FILTERTEST-vector-v7-9.yml
    experiments/configs/2025-11-21-FILTERTEST-vector-v7.yml
    experiments/configs/2025-11-21-FILTERTEST-vector-v8.yml
    experiments/configs/2025-11-22-FILTERTEST-generative-v4.yml
    experiments/configs/2025-11-26-FILTERTEST-generative-v4.yml
    experiments/configs/2025-11-26-FILTERTEST-generative-v5-more-inclusive.yml
    experiments/configs/2025-11-26-FILTERTEST-generative-v6.yml
    experiments/configs/2025-11-26-FILTERTEST-generative-v7.yml
    experiments/configs/2025-11-26-FILTERTEST-generative-v8.yml
    experiments/configs/2025-11-26-FILTERTEST-generative-v9.yml
    experiments/configs/2025-11-28-FILTERTEST-basic-count-beyes.yml

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

    /usr/local/lib/python3.10/dist-packages/google/api_core/_python_version_support.py:266: FutureWarning:

    You are using a Python version (3.10.12) which Google will stop supporting in new releases of google.api_core once it reaches its end of life (2026-10-04). Please upgrade to the latest Python version, or at least Python 3.11, to continue receiving updates for google.api_core past that date.

    /usr/local/lib/python3.10/dist-packages/tqdm/auto.py:21: TqdmWarning:

    IProgress not found. Please update jupyter and ipywidgets. See https://ipywidgets.readthedocs.io/en/stable/user_install.html

    filter
    False    969
    True      31
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

    /tmp/ipykernel_316379/2248653284.py:26: FutureWarning:

    Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version. Call result.infer_objects(copy=False) instead. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`

    /tmp/ipykernel_316379/2248653284.py:26: FutureWarning:

    Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version. Call result.infer_objects(copy=False) instead. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`

    /tmp/ipykernel_316379/2248653284.py:26: FutureWarning:

    Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version. Call result.infer_objects(copy=False) instead. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`

    /tmp/ipykernel_316379/2248653284.py:26: FutureWarning:

    Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version. Call result.infer_objects(copy=False) instead. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`

    /tmp/ipykernel_316379/2248653284.py:26: FutureWarning:

    Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version. Call result.infer_objects(copy=False) instead. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`

    /tmp/ipykernel_316379/2248653284.py:26: FutureWarning:

    Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version. Call result.infer_objects(copy=False) instead. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`

    /tmp/ipykernel_316379/2248653284.py:26: FutureWarning:

    Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version. Call result.infer_objects(copy=False) instead. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`

    /tmp/ipykernel_316379/2248653284.py:26: FutureWarning:

    Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version. Call result.infer_objects(copy=False) instead. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`

    /tmp/ipykernel_316379/2248653284.py:26: FutureWarning:

    Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version. Call result.infer_objects(copy=False) instead. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`

    /tmp/ipykernel_316379/2248653284.py:26: FutureWarning:

    Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version. Call result.infer_objects(copy=False) instead. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`

    /tmp/ipykernel_316379/2248653284.py:26: FutureWarning:

    Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version. Call result.infer_objects(copy=False) instead. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`

    /tmp/ipykernel_316379/2248653284.py:26: FutureWarning:

    Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version. Call result.infer_objects(copy=False) instead. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`

    /tmp/ipykernel_316379/2248653284.py:26: FutureWarning:

    Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version. Call result.infer_objects(copy=False) instead. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`

    /tmp/ipykernel_316379/2248653284.py:26: FutureWarning:

    Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version. Call result.infer_objects(copy=False) instead. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`

    /tmp/ipykernel_316379/2248653284.py:26: FutureWarning:

    Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version. Call result.infer_objects(copy=False) instead. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`

    /tmp/ipykernel_316379/2248653284.py:26: FutureWarning:

    Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version. Call result.infer_objects(copy=False) instead. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`

    /tmp/ipykernel_316379/2248653284.py:26: FutureWarning:

    Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version. Call result.infer_objects(copy=False) instead. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`

    /tmp/ipykernel_316379/2248653284.py:26: FutureWarning:

    Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version. Call result.infer_objects(copy=False) instead. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`

    /tmp/ipykernel_316379/2248653284.py:26: FutureWarning:

    Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version. Call result.infer_objects(copy=False) instead. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`

    /tmp/ipykernel_316379/2248653284.py:26: FutureWarning:

    Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version. Call result.infer_objects(copy=False) instead. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`

    /tmp/ipykernel_316379/2248653284.py:26: FutureWarning:

    Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version. Call result.infer_objects(copy=False) instead. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`

    /tmp/ipykernel_316379/2248653284.py:26: FutureWarning:

    Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version. Call result.infer_objects(copy=False) instead. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`

    /tmp/ipykernel_316379/2248653284.py:26: FutureWarning:

    Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version. Call result.infer_objects(copy=False) instead. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`

    /tmp/ipykernel_316379/2248653284.py:26: FutureWarning:

    Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version. Call result.infer_objects(copy=False) instead. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`

    /tmp/ipykernel_316379/2248653284.py:26: FutureWarning:

    Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version. Call result.infer_objects(copy=False) instead. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`

    /tmp/ipykernel_316379/2248653284.py:26: FutureWarning:

    Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version. Call result.infer_objects(copy=False) instead. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`

    /tmp/ipykernel_316379/2248653284.py:26: FutureWarning:

    Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version. Call result.infer_objects(copy=False) instead. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`

    /tmp/ipykernel_316379/2248653284.py:26: FutureWarning:

    Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version. Call result.infer_objects(copy=False) instead. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`

    /tmp/ipykernel_316379/2248653284.py:26: FutureWarning:

    Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version. Call result.infer_objects(copy=False) instead. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`

    /tmp/ipykernel_316379/2248653284.py:26: FutureWarning:

    Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version. Call result.infer_objects(copy=False) instead. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`

    /tmp/ipykernel_316379/2248653284.py:26: FutureWarning:

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
execution_count="4">

|  |  | accuracy | precision | recall | f1 |
|----|----|---:|---:|---:|---:|
| 21 | experiments/configs/2025-11-20-FILTERTEST-vector-v1.yml | 0.969 | 0 | 0 | 0 |
| 16 | experiments/configs/2025-11-21-FILTERTEST-vector-v7-9.yml | 0.969 | 0 | 0 | 0 |
| 29 | experiments/configs/2025-11-20-FILTERTEST-vector-v2-lower-threshold.yml | 0.949 | 0.115385 | 0.0967742 | 0.105263 |
| 1 | experiments/configs/2025-11-21-FILTERTEST-vector-v7-8.yml | 0.971 | 1 | 0.0645161 | 0.121212 |
| 25 | experiments/configs/2025-11-21-FILTERTEST-vector-v6.yml | 0.971 | 1 | 0.0645161 | 0.121212 |
| 7 | experiments/configs/2025-11-21-FILTERTEST-vector-v8.yml | 0.971 | 1 | 0.0645161 | 0.121212 |
| 27 | experiments/configs/2025-11-21-FILTERTEST-vector-v7.yml | 0.971 | 1 | 0.0645161 | 0.121212 |
| 9 | experiments/configs/2025-11-21-FILTERTEST-vector-v7-5.yml | 0.721 | 0.0810811 | 0.774194 | 0.146789 |
| 18 | experiments/configs/2025-11-21-FILTERTEST-vector-v4-rm_strings.yml | 0.892 | 0.133333 | 0.451613 | 0.205882 |
| 12 | experiments/configs/2025-11-21-FILTERTEST-vector-v5.yml | 0.861 | 0.130137 | 0.612903 | 0.214689 |
| 11 | experiments/configs/2025-11-21-FILTERTEST-vector-v7-6.yml | 0.939 | 0.232143 | 0.419355 | 0.298851 |
| 28 | experiments/configs/2025-11-19-FILTERTEST-e-or-p.yml | 0.973 | 0.75 | 0.193548 | 0.307692 |
| 15 | experiments/configs/2025-11-21-FILTERTEST-vector-v3-new-strings.yml | 0.969 | 0.5 | 0.225806 | 0.311111 |
| 20 | experiments/configs/2025-11-21-FILTERTEST-vector-v7-7.yml | 0.975 | 1 | 0.193548 | 0.324324 |
| 10 | experiments/configs/2025-11-17-FILTERTEST-simple.yml | 0.975 | 1 | 0.193548 | 0.324324 |
| 5 | experiments/configs/2025-11-19-FILTERTEST-add-techs.yml | 0.973 | 0.7 | 0.225806 | 0.341463 |
| 19 | experiments/configs/2025-11-21-FILTERTEST-generative-v1.yml | 0.924 | 0.277228 | 0.903226 | 0.424242 |
| 13 | experiments/configs/2025-11-28-FILTERTEST-basic-count-beyes.yml | 0.979 | 0.857143 | 0.387097 | 0.533333 |
| 22 | experiments/configs/2025-11-26-FILTERTEST-generative-v5-more-inclusive.yml | 0.967 | 0.481481 | 0.83871 | 0.611765 |
| 0 | experiments/configs/2025-11-26-FILTERTEST-generative-v6.yml | 0.98 | 0.72 | 0.580645 | 0.642857 |
| 26 | experiments/configs/2025-11-21-FILTERTEST-generative-v2.yml | 0.981 | 0.75 | 0.580645 | 0.654545 |
| 3 | experiments/configs/2025-11-21-FILTERTEST-generative-v3-two-step.yml | 0.983 | 0.769231 | 0.645161 | 0.701754 |
| 4 | experiments/configs/2025-11-19-FILTERTEST-add-techs-l2-and-orgs-and-sites-v2.yml | 0.98 | 0.622222 | 0.903226 | 0.736842 |
| 2 | experiments/configs/2025-11-26-FILTERTEST-generative-v7.yml | 0.988 | 0.913043 | 0.677419 | 0.777778 |
| 30 | experiments/configs/2025-11-26-FILTERTEST-generative-v4.yml | 0.987 | 0.764706 | 0.83871 | 0.8 |
| 17 | experiments/configs/2025-11-26-FILTERTEST-generative-v8.yml | 0.988 | 0.806452 | 0.806452 | 0.806452 |
| 8 | experiments/configs/2025-11-19-FILTERTEST-add-techs-l2-and-orgs-and-sites.yml | 0.987 | 0.736842 | 0.903226 | 0.811594 |
| 6 | experiments/configs/2025-11-22-FILTERTEST-generative-v4.yml | 0.988 | 0.771429 | 0.870968 | 0.818182 |
| 23 | experiments/configs/2025-11-19-FILTERTEST-add-techs-l2.yml | 0.988 | 0.771429 | 0.870968 | 0.818182 |
| 24 | experiments/configs/2025-11-19-FILTERTEST-add-techs-l2-and-orgs.yml | 0.988 | 0.756757 | 0.903226 | 0.823529 |
| 14 | experiments/configs/2025-11-26-FILTERTEST-generative-v9.yml | 0.99 | 0.783784 | 0.935484 | 0.852941 |

</div>

</div>

``` python
# 1. Best filter with highest F1
best_config ='experiments/results/2025-11-26-FILTERTEST-generative-v8.yml'
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

    /tmp/ipykernel_316379/4185210660.py:14: FutureWarning:

    Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version. Call result.infer_objects(copy=False) instead. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`

|  | id | title | filter | filter_pred |
|----|---:|:---|:---|:---|
| 88 | 1662001 | STATEMENTS BY MEMBERS, 25twoZERO Movement | False | True |
| 121 | 2570478 | ANSWERS TO QUESTIONS, Light Dues | False | True |
| 185 | 1900666 | QUESTIONS WITHOUT NOTICE, FRENCH ATOMIC ENERGY COMMISSION | True | False |
| 241 | 1256676 | JABILUKA URANIUM MINE, COMMITTEES, Privileges Committee, Report | False | True |
| 297 | 1301272 | QUESTIONS WITHOUT NOTICE, MARALINGA NUCLEAR TESTS | False | True |
| 391 | 2334141 | ANSWERS TO QUESTIONS, Liquid Fuels-: Production from Fruit. | True | False |
| 524 | 1909459 | ANSWERS TO QUESTIONS UPON NOTICE, Transmission Equipment (Question 1249) | False | True |
| 583 | 1678291 | PRIVATE MEMBERS’ BUSINESS, Global Methane Pledge | False | True |
| 603 | 1610777 | CONSTITUENCY STATEMENTS, BP Australia | True | False |
| 626 | 2486412 | ANSWERS TO QUESTIONS, Civil Aviation : Petrol Tax. | True | False |
| 726 | 1578773 | QUESTIONS WITHOUT NOTICE, Dobell Electorate: Mining | True | False |
| 817 | 1818012 | BILLS, Security of Critical Infrastructure Bill 2017, Security of Critical Infrastructure (Consequential and Transitional Provisions) Bill 2017, Second Reading | True | False |
