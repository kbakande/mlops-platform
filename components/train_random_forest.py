from config.config import base_image
from kfp.v2 import dsl
from kfp.v2.dsl import Dataset, Input, Model, Output

@dsl.component(base_image=base_image)
def train_random_forest(
    train_dataset: Input[Dataset], 
    model: Output[Model]
):
    """
    Train a Random Forest model with Random Search.
    """

    import pandas as pd
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.model_selection import RandomizedSearchCV
    from sklearn.metrics import accuracy_score
    from sklearn.pipeline import Pipeline
    from sklearn.compose import ColumnTransformer
    from sklearn.preprocessing import StandardScaler, OneHotEncoder
    import joblib
    import logging

    logging.basicConfig(level=logging.INFO)

    train_df = pd.read_csv(train_dataset.path)

    X_train = train_df.iloc[:, :-1]
    y_train = train_df.iloc[:, -1]

    numeric_transformer = Pipeline(steps=[('scaler', StandardScaler())])
    categorical_transformer = Pipeline(steps=[('onehot', OneHotEncoder(handle_unknown='ignore'))])

    numeric_features = X_train.select_dtypes(include=['int64', 'float64']).columns
    categorical_features = X_train.select_dtypes(include=['object', 'category']).columns

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_features),
            ('cat', categorical_transformer, categorical_features)
        ])

    classifier = RandomForestClassifier(random_state=0)

    pipeline = Pipeline(steps=[('preprocessor', preprocessor), ('classifier', classifier)])

    param_distributions = {
        'classifier__n_estimators': [10, 50, 100, 200],
        'classifier__max_depth': [None, 10, 20, 30],
        'classifier__min_samples_split': [2, 5, 10],
        'classifier__min_samples_leaf': [1, 2, 4]
    }

    random_search = RandomizedSearchCV(pipeline, param_distributions, n_iter=20, cv=5, n_jobs=-1, random_state=0)

    random_search.fit(X_train, y_train)

    y_train_pred = random_search.predict(X_train)
    training_accuracy = accuracy_score(y_train, y_train_pred)
    logging.info(f"Training Accuracy: {training_accuracy}")

    best_model = random_search.best_estimator_
    logging.info(f"Best Parameters: {random_search.best_params_}")

    model.metadata["framework"] = "RandomForest"
    model.metadata["metrics"] = {
        "best_score": random_search.best_score_,
        "training_accuracy": training_accuracy
    }

    file_name = model.path + ".joblib"
    joblib.dump(best_model, file_name)