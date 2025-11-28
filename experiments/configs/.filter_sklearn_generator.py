import itertools
import yaml
from pathlib import Path

OUTPUT_DIR = Path("experiments/configs")
OUTPUT_DIR.mkdir(exist_ok=True)

# ------------------------------------------------------------
# SEARCH SPACE — Add/remove entries here to scale up/down
# ------------------------------------------------------------

# Multiple n-gram configurations
NGRAMS = [
    (1,1),
    (1,2),
    (1,3),
]

VECTORISERS = [

    # CountVectorizer sweeps
    *[
        (
            "sklearn.feature_extraction.text.CountVectorizer",
            {"ngram_range": ngram, "min_df": min_df}
        )
        for ngram in NGRAMS
        for min_df in [1, 2, 3, 5]
    ],

    # TF-IDF sweeps
    *[
        (
            "sklearn.feature_extraction.text.TfidfVectorizer",
            {
                "ngram_range": ngram,
                "min_df": min_df,
                "use_idf": use_idf,
                "smooth_idf": smooth
            }
        )
        for ngram in NGRAMS
        for min_df in [1, 2, 3]
        for use_idf in [True, False]
        for smooth in [True, False]
    ],

    # HashingVectorizer (no fitting)
    *[
        (
            "sklearn.feature_extraction.text.HashingVectorizer",
            {
                "ngram_range": ngram,
                "n_features": n_features,
                "alternate_sign": alt_sign
            }
        )
        for ngram in NGRAMS
        for n_features in [2**16, 2**18, 2**20]
        for alt_sign in [True, False]
    ],
]


CLASSIFIERS = [

    # Naive Bayes
    ("sklearn.naive_bayes.MultinomialNB",
        {"alpha": 0.1}),
    ("sklearn.naive_bayes.MultinomialNB",
        {"alpha": 0.5}),
    ("sklearn.naive_bayes.MultinomialNB",
        {"alpha": 1.0}),

    # Logistic Regression
    *[
        (
            "sklearn.linear_model.LogisticRegression",
            {
                "max_iter": 300,
                "C": C,
                "penalty": penalty,
                "solver": solver
            }
        )
        for C in [0.1, 1.0, 3.0, 10.0]
        for penalty, solver in [
            ("l2", "lbfgs"),
            ("l2", "liblinear"),
        ]
    ],

    # Linear SVM
    *[
        (
            "sklearn.svm.LinearSVC",
            {
                "C": C,
                "loss": loss,
                "max_iter": 5000
            }
        )
        for C in [0.5, 1.0, 2.0, 5.0]
        for loss in ["hinge", "squared_hinge"]
    ],

    # SGDClassifier (linear models)
    *[
        (
            "sklearn.linear_model.SGDClassifier",
            {
                "loss": loss,
                "alpha": alpha,
                "max_iter": 2000
            }
        )
        for loss in ["hinge", "log_loss", "modified_huber"]
        for alpha in [1e-4, 1e-3, 1e-2]
    ],

    # Random Forest
    *[
        (
            "sklearn.ensemble.RandomForestClassifier",
            {
                "n_estimators": n_est,
                "max_depth": depth,
            }
        )
        for n_est in [100, 200, 400]
        for depth in [None, 10, 20]
    ],

    # ExtraTrees
    *[
        (
            "sklearn.ensemble.ExtraTreesClassifier",
            {
                "n_estimators": n_est,
                "criterion": crit
            }
        )
        for n_est in [100, 300]
        for crit in ["gini", "entropy"]
    ],

    # Gradient Boosting
    *[
        (
            "sklearn.ensemble.GradientBoostingClassifier",
            {
                "n_estimators": n_est,
                "learning_rate": lr
            }
        )
        for n_est in [50, 100]
        for lr in [0.05, 0.1]
    ],
]

TRAINING_DATA = "data/synthetic/25k_generative_filter_output/training_data.csv"
LABELED_DATA = "data/labeled/filter/labeled_examples.pkl"

# ------------------------------------------------------------
# Helper functions
# ------------------------------------------------------------

def sanitise(value):
    """Make dict values filesystem-safe for filenames."""
    if isinstance(value, tuple):
        return "x".join(str(v) for v in value)
    return str(value).replace(" ", "").replace("'", "").replace("{","").replace("}","")


def create_config(vectoriser, classifier):
    vec_model, vec_args = vectoriser
    clf_model, clf_args = classifier

    return {
        "data": {
            "file": LABELED_DATA
        },
        "filter": {
            "ScikitFilter": {
                "training_data_path": TRAINING_DATA,
                "embedding_model": vec_model,
                "embedding_args": vec_args,
                "classifier_model": clf_model,
                "classifier_args": clf_args,
            }
        }
    }


def main():
    combos = list(itertools.product(VECTORISERS, CLASSIFIERS))
    print(f"Generating {len(combos)} experiment configs...")

    for i, (vec, clf) in enumerate(combos):
        vec_model, vec_args = vec
        clf_model, clf_args = clf

        vec_name = vec_model.split(".")[-1]
        clf_name = clf_model.split(".")[-1]

        vec_args_str = "_".join([f"{k}-{sanitise(v)}" for k, v in vec_args.items()]) or "default"
        clf_args_str = "_".join([f"{k}-{sanitise(v)}" for k, v in clf_args.items()]) or "default"

        filename = f"2025-11-28-FILTERTEST-{vec_name}-{vec_args_str}-{clf_name}-{clf_args_str}.yaml"
        filepath = OUTPUT_DIR / filename

        config = create_config(vec, clf)
        with filepath.open("w") as f:
            yaml.dump(config, f, sort_keys=False)

    print("Done. All experiment configs generated.")


if __name__ == "__main__":
    main()
