
from config.config import base_image, gcs_url
from kfp.v2 import dsl
from kfp.v2.dsl import Dataset, Output

@dsl.component(base_image=base_image) 
def load_data(gcs_url: str, 
              output_dataset: Output[Dataset]
              ):
    """
    Download data from a GCS URL and save it to the specified path as a Dataset.
    """

    from google.cloud import storage
    import pandas as pd

    if not gcs_url.startswith("gs://"):
        raise ValueError("Invalid GCS URL format")
    parts = gcs_url[5:].split("/", 1)
    if len(parts) != 2:
        raise ValueError("Invalid GCS URL format")
    bucket_name, blob_name = parts

    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    df = pd.read_csv(blob.open("rb"))

    df.to_csv(output_dataset.path, index=False)
    output_dataset.metadata['dataset_metadata'] = {'format': 'csv'}
