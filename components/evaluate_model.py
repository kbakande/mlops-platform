from config.config import base_image
from kfp.v2 import dsl
from typing import NamedTuple
from kfp.v2.dsl import Dataset, Input, Model, Metrics

@dsl.component(base_image=base_image)
def evaluate_model(
    test_dataset: Input[Dataset], 
    dt_model: Input[Model],
    rf_model: Input[Model],
) -> NamedTuple("EvaluationOutput", [("optimal_model", str)]):
    """
    Evaluate models on test data and determine the best one based on accuracy.
    """
    # Import necessary libraries within the function
    import pandas as pd
    import joblib
    import sklearn.metrics as skmetrics
    import logging

    # Set up logging
    logging.basicConfig(level=logging.INFO)

    def load_model(model_dir):
        """Load a model from a specified directory."""
        model_path = model_dir.path + ".joblib"
        return joblib.load(model_path)

    def evaluate(model, X, y):
        """Evaluate a model and return the accuracy score."""
        predictions = model.predict(X)
        return skmetrics.accuracy_score(y, predictions)

    # Load the test dataset
    df = pd.read_csv(test_dataset.path)
    X_test = df.iloc[:, :-1]
    y_test = df.iloc[:, -1]

    # Convert categorical columns to 'category' data type for X_test
    categorical_cols = X_test.select_dtypes(include=['object']).columns
    X_test[categorical_cols] = X_test[categorical_cols].astype('category')

    # Load models
    dt = load_model(dt_model)
    rf = load_model(rf_model)

    # Evaluate models
    dt_accuracy = evaluate(dt, X_test, y_test)
    rf_accuracy = evaluate(rf, X_test, y_test)

    # Log metrics
    logging.info(f"Decision Tree Accuracy: {dt_accuracy}")
    logging.info(f"Random Forest Accuracy: {rf_accuracy}")

    # Determine the best model
    # You can modify the logic here to compare all your models
    optimal_model = "decision_tree" if dt_accuracy > rf_accuracy else "random_forest"
    optimal_accuracy = max(dt_accuracy, rf_accuracy)
    logging.info(f"Optimal Model: {optimal_model} with accuracy: {optimal_accuracy}")

    return (optimal_model,)
