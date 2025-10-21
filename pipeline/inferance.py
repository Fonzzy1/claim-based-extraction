import yaml
import sys
import importlib
from prisma import Client
from models.extractor import Processor
import os
from models.data_structure import Document, Corpus



if len(sys.argv) < 2:
    print("Error: Config file not specified.")
    sys.exit(1)

config_file = sys.argv[1]

config_file = "experiments/configs/2025-10-25-demo.yml"
with open(config_file, "r") as file:
    config = yaml.safe_load(file)

out_folder = os.path.join(
    "experiments", "results", os.path.splitext(config_file.split("/")[-1])[0]
)

if os.path.exists(out_folder):
    raise Exception("Config has already been run")

os.mkdir(out_folder)

## Pull in the data
data_config = config["data"]
if "query" in data_config.keys():
    db = Client()
    await db.connect()
    raw_data = await db.query_raw(data_config["query"])
    data = Corpus([Document(**x) for x in raw_data])


## Filter the data
filter_config = config["filter"]
filter_class_name = list(filter_config.keys())[0]
module = importlib.import_module("models.filter")
filter_class = getattr(module, filter_class_name)

if "file" in filter_config.keys():
    filter = filter_class.load_from_file(filter_config["file"])
elif "drive" in filter_config.keys():
    filter = filter_class.load_from_drive(filter_config["drive"])
else:
    filter = filter_class(**filter_config[filter_class_name])

data = filter.transform(data)

# Preprocess the data
processor_config = config["processor"]
context_size = processor_config["context_size"]
parts = processor_config["sentence_splitting_function"].split(".")
module = ".".join(parts[:-1])
function = parts[-1]
sentence_splitting_function = importlib.import_module(module).__getattribute__(
    function
)
processor = Processor(context_size, sentence_splitting_function)
data = processor.transform(data)

# Extract the data into sentences
extractor_config = config["extractor"]
extractor_class_name = list(extractor_config.keys())[0]
module = importlib.import_module("models.extractor")
extractor_class = getattr(module, extractor_class_name)

if "file" in extractor_config.keys():
    extractor = extractor_class.load_from_file(extractor_config["file"])
elif "drive" in extractor_config.keys():
    extractor = extractor_class.load_from_drive(extractor_config["drive"])
else:
    extractor = extractor_class(**extractor_config[extractor_class_name])

data = extractor.transform(data)

# Deconstruct these
deconstructor_config = config["deconstructor"]
deconstructor_class_name = list(deconstructor_config.keys())[0]
module = importlib.import_module("models.deconstructor")
deconstructor_class = getattr(module, deconstructor_class_name)

if "file" in deconstructor_config.keys():
    deconstructor = deconstructor_class.load_from_file(
        deconstructor_config["file"]
    )
elif "drive" in deconstructor_config.keys():
    deconstructor = deconstructor_class.load_from_drive(
        deconstructor_config["drive"]
    )
else:
    deconstructor = deconstructor_class(
        **deconstructor_config[deconstructor_class_name]
    )

data = deconstructor.transform(data)

print(data)
