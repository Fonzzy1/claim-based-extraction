from models.base_model import ISSUE_TAXONOMY, TECH_TAXONOMY
import itertools
from openai import OpenAI
from tqdm import tqdm
import numpy as np

client = OpenAI()
model = "text-embedding-3-small"


all_techs = []
for k, d in TECH_TAXONOMY.items():
    all_techs.append(k)
    for v in d.keys():
        all_techs.append(v)
all_issues = []
for k, d in ISSUE_TAXONOMY.items():
    all_issues.append(k)
    for v in d:
        all_issues.append(v)

# === SENTENCE TEMPLATES ===
templates = [
    "Policies supporting {tech} affect {issue}.",
    "Investment in {tech} influences {issue}.",
    "Regulations on {tech} impact {issue}.",
    "Subsidies for {tech} shape {issue}.",
    "{tech} development determines {issue}.",
    "Government funding for {tech} changes {issue}.",
    "Energy planning around {tech} affects {issue}.",
    "{tech} adoption will influence {issue}.",
    "Strategic investment in {tech} could improve {issue}.",
    "Policy shifts regarding {tech} will affect {issue}.",
]

sentences = [
    template.format(tech=tech, issue=issue)
    for template, tech, issue in itertools.product(
        templates, all_techs, all_issues
    )
]

with open("data/synthetic/semantic_filter/sentences.txt", "w") as f:
    for sentence in sentences:
        f.write(sentence + "\n")

all_embeddings = []
for i in tqdm(range(0, len(sentences), 50)):
    chunk = sentences[i : i + 50]
    response = client.embeddings.create(input=chunk, model=model)
    embeddings = [row.embedding for row in response.data]
    all_embeddings.append(np.array(embeddings))
all_embeddings = np.vstack(all_embeddings)
rowwise_avg = np.mean(all_embeddings, axis=1)
np.savetxt(
    f"data/synthetic/semantic_filter/embeddings_{model}.txt",
    rowwise_avg,
    delimiter=",",
)
