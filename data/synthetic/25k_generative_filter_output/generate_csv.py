from models.base_model import Corpus
import os
import pandas as pd


if os.path.basename(os.getcwd()) != "claim-based-extraction":
    os.chdir("../../")

all_texts = Corpus.load_from_file(
    "experiments/results/2025-11-26-25k-articles-for-labeling.pkl"
)
df = pd.DataFrame(
    [{"X": doc.title, "id": doc.id} for doc in all_texts.documents]
)

filtered_texts = Corpus.load_from_file(
    "experiments/results/2025-11-27-25k-with-gen-v9.pkl"
)

filtered_ids = [x.id for x in filtered_texts.documents]

df["y"] = df.id.apply(lambda x: 1 if x in filtered_ids else 0)


df[['X','y']].to_csv("data/synthetic/25k_generative_filter_output/training_data.csv")
