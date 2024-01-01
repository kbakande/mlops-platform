from config.config import base_image, train_ratio
from kfp.v2 import dsl
from kfp.v2.dsl import Dataset, Input, Output

@dsl.component(base_image=base_image)
def preprocess_data(
    input_dataset: Input[Dataset], 
    train_dataset: Output[Dataset],
    test_dataset: Output[Dataset]
):
    """
    Preprocess data by partitioning it into training and testing sets.
    """
    # Import necessary libraries within the function
    import pandas as pd
    from sklearn.model_selection import train_test_split

    # Load dataset
    df = pd.read_csv(input_dataset.path)
    df = df.dropna()

    # Check if the last column is the target and contains 'Yes'/'No', then convert it to 1/0
    if set(df.iloc[:, -1].unique()) == {'Yes', 'No'}:
        df.iloc[:, -1] = df.iloc[:, -1].map({'Yes': 1, 'No': 0})

    # Splitting data into training and testing sets
    train_data, test_data = train_test_split(df, train_size=train_ratio, random_state=42)

    # Saving the datasets
    train_data.to_csv(train_dataset.path, index=False)
    test_data.to_csv(test_dataset.path, index=False)