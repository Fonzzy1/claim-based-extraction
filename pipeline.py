import yaml
import asyncio
import sys
import importlib
import os
from models.base_model import Document, Corpus
import asyncio

if len(sys.argv) < 2:
    print("Error: Config file not specified.")
    sys.exit(1)

config_file = sys.argv[1]

def main(config_file):

    print("Loading Config ...")

    with open(config_file, "r") as file:
        config = yaml.safe_load(file)

    print("Pulling Data")
    data_config = config["data"]
    if "query" in data_config.keys():
        data = Corpus.from_query(data_config['query'], os.environ['DATABASE_URL'])
    elif "file" in data_config.keys():
        data = Corpus.load_from_file(data_config["file"])
    elif "strings" in data_config.keys():
        data = Corpus.from_file_of_strings(data_config["strings"])
    else:
        raise Exception("No valid datasouce")

    print("Contructing Processor")
    # Process the data into sentences
    processor_config = config.get("processor")
    if not processor_config:
        return data
    processor_class_name = list(processor_config.keys())[0]
    module = importlib.import_module("models.processor")
    processor_class = getattr(module, processor_class_name)

    if "file" in processor_config.keys():
        processor = processor_class.load_from_file(processor_config["file"])
    else:
        processor = processor_class(**processor_config[processor_class_name])

    print("Processing Sentences ...")
    data = processor.transform(data)


    # Classify these
    print("Constructing Classifier")
    classifier_config = config.get("classifier")
    if not classifier_config:
        return data
    classifier_class_name = list(classifier_config.keys())[0]
    module = importlib.import_module("models.classifier")
    classifier_class = getattr(module, classifier_class_name)

    if "file" in classifier_config.keys():
        classifier = classifier_class.load_from_file(
            classifier_config["file"]
        )
    else:
        classifier = classifier_class(
            **classifier_config[classifier_class_name]
        )

    print("Classifying Claims ...")
    data = classifier.transform(data)

    return data


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Error: Config file not specified.")
        sys.exit(1)

    config_file = sys.argv[1]

    out_file = os.path.join(
        "experiments",
        "results",
        os.path.splitext(config_file.split("/")[-1])[0] + ".pkl",
    )
    if os.path.exists(out_file):
        raise Exception("Outfile allready exists on disk")

    data = main(config_file)
    data.save_to_file(out_file)
