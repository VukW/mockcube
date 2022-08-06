import argparse
import yaml
import os
import numpy as np


class Evaluation:
    def __init__(self, preds_path, labels_path, parameters_file, output_file):
        with open(parameters_file, "r") as f:
            self.params = yaml.full_load(f)

        self.output_file = output_file
        self.preds_path = preds_path
        self.labels_path = labels_path

    def run(self):
        labels = (
            open(os.path.join(self.labels_path, "ans.csv")).read().strip().split("\n")
        )
        labels = list(map(int, labels))
        preds = (
            open(os.path.join(self.preds_path, "preds.txt")).read().strip().split("\n")
        )
        preds = list(map(int, preds))

        correct = sum(pred == label for pred, label in zip(preds, labels))
        incorrect = len(preds) - correct
        error = incorrect / correct if correct != 0 else np.nan
        with open(self.output_file, "w") as f:
            yaml.dump(
                {
                    "correct": correct,
                    "incorrect": incorrect,
                    "error": error,
                    "num_classes": self.params["num_classes"],
                },
                f,
            )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--preds_path",
        "--preds-path",
        type=str,
        required=True,
        help="folder containing the labels and preds",
    )

    parser.add_argument(
        "--labels_path",
        "--labels-path",
        type=str,
        required=True,
        help="folder containing the labels and preds",
    )

    parser.add_argument(
        "--output_file",
        "--output-file",
        type=str,
        required=True,
        help="file to store metrics results as YAML",
    )
    parser.add_argument(
        "--parameters_file",
        "--parameters-file",
        type=str,
        required=True,
        help="File containing parameters for evaluation",
    )
    args = parser.parse_args()

    evaluator = Evaluation(
        args.preds_path, args.labels_path, args.parameters_file, args.output_file
    )

    evaluator.run()
