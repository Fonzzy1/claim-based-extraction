from models.base_model import Corpus
import questionary
import os

data = Corpus.load_from_file("./data/labeled/filter/labeled_examples.pkl")


for i,document in enumerate(data.documents):
    os.system("clear")
    if not hasattr(document, "filter"):
        print(i)
        print(document.title)
        while True:
            answer = (
                input("Is this part of the filter? (y/n/? for text): ")
                .strip()
                .lower()
            )
            if answer == "?":
                print(document.text)
            elif answer in ["y", "n"]:
                document.filter = answer == "y"
                break


os.remove("./data/labeled/filter/labeled_examples.pkl")
data.save_to_file("./data/labeled/filter/labeled_examples.pkl")
