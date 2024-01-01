# components/train_decision_tree.py
from config.config import base_image
from kfp.v2 import dsl
from kfp.v2.dsl import Dataset, Input, Model, Output

@dsl.component(base_image=base_image)
def train_decision_tree(
    train_dataset: Input[Dataset], 
    model: Output[Model]
):
    """
    Train a Decision Tree model with Random Search.
    """
    # Import necessary libraries within the function
    import pandas as pd
    from sklearn.tree import DecisionTreeClassifier
    from sklearn.model_selection import RandomizedSearchCV
    from sklearn.metrics import accuracy_score
    from sklearn.pipeline import Pipeline
    from sklearn.compose import ColumnTransformer
    from sklearn.preprocessing import StandardScaler, OneHotEncoder
    import joblib
    import logging

    # Set up logging
    logging.basicConfig(level=logging.INFO)

    # Load training dataset
    train_df = pd.read_csv(train_dataset.path)

    # Separate features and target. Assuming target is the last column.
    X_train = train_df.iloc[:, :-1]
    y_train = train_df.iloc[:, -1]

    # Preprocess features
    numeric_transformer = Pipeline(steps=[('scaler', StandardScaler())])
    categorical_transformer = Pipeline(steps=[('onehot', OneHotEncoder(handle_unknown='ignore'))])

    numeric_features = X_train.select_dtypes(include=['int64', 'float64']).columns
    categorical_features = X_train.select_dtypes(include=['object', 'category']).columns

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_features),
            ('cat', categorical_transformer, categorical_features)
        ])

    # Decision Tree classifier
    classifier = DecisionTreeClassifier(random_state=0)

    # Pipeline
    pipeline = Pipeline(steps=[('preprocessor', preprocessor), ('classifier', classifier)])

    # Define search space for hyperparameters
    param_distributions = {
        'classifier__max_depth': [None, 10, 20, 30],
        'classifier__min_samples_split': [2, 5, 10],
        'classifier__min_samples_leaf': [1, 2, 4],
        'classifier__max_features': [None, 'auto', 'sqrt', 'log2']
    }

    # Random search with cross-validation
    random_search = RandomizedSearchCV(pipeline, param_distributions, n_iter=20, cv=5, n_jobs=-1, random_state=0)

    # Train the model
    random_search.fit(X_train, y_train)

    # Calculate training accuracy
    y_train_pred = random_search.predict(X_train)
    training_accuracy = accuracy_score(y_train, y_train_pred)
    logging.info(f"Training Accuracy: {training_accuracy}")

    # Best model
    best_model = random_search.best_estimator_
    logging.info(f"Best Parameters: {random_search.best_params_}")

    model.metadata["framework"] = "DecisionTree"
    model.metadata["metrics"] = {
        "best_score": random_search.best_score_,
        "training_accuracy": training_accuracy
    }

    # Save the model using joblib
    file_name = model.path + ".joblib"
    joblib.dump(best_model, file_name)