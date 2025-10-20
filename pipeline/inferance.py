import yaml
import sys
import importlib
from prisma import Client

with open("experiments/configs/2025-10-25-demo.yml", "r") as f:
    config = yaml.safe_load(f)

## Pull in the data
data_config = config["data"]
if "query" in data_config.keys():
    db = Client()
    await db.connect()
    data = db.query_raw(data_config["query"])

## Filter the data
filter_config = config["filter"]
filter_class_name = list(filter_config.keys())[0]
module = importlib.import_module("models.filter")
filter_class = getattr(module, filter_class_name)

if (
    "file" not in filter_config.values()
    and "drive" not in filter_config.values()
):
    filter = filter_class(**filter_config[filter_class_name])
