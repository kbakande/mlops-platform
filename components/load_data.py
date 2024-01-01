from config.config import base_image, gcs_url
from kfp.v2 import dsl
from kfp.v2.dsl import Dataset, Output

@dsl.component(base_image=base_image)
def load_data(output_dataset: Output[Dataset]):
    """
    Download data from a GCS URL and save it to the specified path as a Dataset.
    """
    # Import necessary libraries within the function
    from google.cloud import storage
    import pandas as pd

    # Extract bucket and blob info from GCS URL
    if not gcs_url.startswith("gs://"):
        raise ValueError("Invalid GCS URL format")
    parts = gcs_url[5:].split("/", 1)
    if len(parts) != 2:
        raise ValueError("Invalid GCS URL format")
    bucket_name, blob_name = parts

    # Create a GCS client
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    # Read the contents into Pandas DataFrame
    df = pd.read_csv(blob.open("rb"))

    # Save to the specified path as Dataset
    df.to_csv(output_dataset.path, index=False)
    output_dataset.metadata['dataset_metadata'] = {'format': 'csv'}