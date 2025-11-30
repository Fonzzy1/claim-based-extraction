import importlib
from models.filter.base_filter import Filter
from sklearn.feature_extraction import text as extraction_module
import pandas as pd
from sklearn.pipeline import make_pipeline


def string_to_class(string):
    module_name, class_name = (
        ".".join(string.split(".")[:-1]),
        string.split(".")[-1],
    )
    module = importlib.import_module(module_name)
    cls = getattr(module, class_name)
    return cls


def lists_to_tuples(d):
    """
    Recursively convert all lists inside a dict into tuples.
    Leaves non-list values unchanged.
    """
    for k, v in d.items():
        if isinstance(v, list):
            d[k] = tuple(
                (
                    lists_to_tuples(x)
                    if isinstance(x, dict)
                    else tuple(x) if isinstance(x, list) else x
                )
                for x in v
            )
        elif isinstance(v, dict):
            d[k] = lists_to_tuples(v)
    return d


class ScikitFilter(Filter):
    def __init__(
        self,
        training_data_path,
        embedding_model,
        embedding_args,
        classifier_model,
        classifier_args,
    ):
        """
        training_data_path: path to a csv with text and 1, 0 bools for include exclude
        embedding model: name of embedding module used in the sklearn.feature_extraction.text  module
        """

        df = pd.read_csv(training_data_path)
        X = df.X.to_list()
        y = df.y.to_list()

        embedding_args = lists_to_tuples(embedding_args)
        classifier_args = lists_to_tuples(classifier_args)

        embedder_class = string_to_class(embedding_model)
        classifier_class = string_to_class(classifier_model)

        self.pipeline = make_pipeline(
            embedder_class(**embedding_args),
            classifier_class(**classifier_args),
        )
        self.pipeline.fit(X, y)

    def infer(self, document):
        prediction = self.pipeline.predict([self._get_feature(document)])
        return bool(prediction[0])
