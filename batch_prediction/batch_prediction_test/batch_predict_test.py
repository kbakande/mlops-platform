import argparse
import os
import pandas as pd
import joblib
from google.cloud import storage, bigquery

def batch_predict(
    model_gcs_path: str, 
    input_data_gcs_path: str, 
    table_ref: str, project: str, 
    target_column=None
):
    """
    Loads data from GCS, obtains predictions, and writes data to BigQuery
    """

    storage_client = storage.Client()
    bucket_name, model_path = model_gcs_path.replace("gs://", "").split("/", 1)
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(model_path)
    model_filename = "/tmp/model.joblib"
    blob.download_to_filename(model_filename)
    model = joblib.load(model_filename)

    data_bucket_name, input_data_path = input_data_gcs_path.replace("gs://", "").split("/", 1)
    data_bucket = storage_client.bucket(data_bucket_name)
    blob = data_bucket.blob(input_data_path)
    input_data_filename = "/tmp/input_data.csv"
    blob.download_to_filename(input_data_filename)
    input_data = pd.read_csv(input_data_filename).sample(4)

    if target_column:
        input_data.drop(columns=[target_column], inplace=True, errors="ignore")
    else:
        input_data = input_data.iloc[:, :-1]

    categorical_cols = input_data.select_dtypes(include=["object"]).columns
    input_data[categorical_cols] = input_data[categorical_cols].astype("category")

    predictions = model.predict(input_data)
    print("Predictions success!")
    print(f"prediction: {predictions}")

    bigquery_client = bigquery.Client(project=project)
    job_config = bigquery.LoadJobConfig(
        schema=[
            bigquery.SchemaField("prediction", "FLOAT"),
        ],
        write_disposition=bigquery.WriteDisposition.WRITE_APPEND,
    )
    job = bigquery_client.load_table_from_dataframe(
        pd.DataFrame({"prediction": predictions}),
        table_ref,
        job_config=job_config,
    )
    job.result() 

    return f"Predictions written to {table_ref}"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Obtain batch prediction from Vertex AI model"
    )
    parser.add_argument("--model_gcs_path", required=True, help="Model GCS path")
    parser.add_argument(
        "--input_data_gcs_path", required=True, help="Input data GCS path"
    )
    parser.add_argument("--table_ref", required=True, help="GCP output data table")
    parser.add_argument("--project", required=True, help="GCP project name")

    args = parser.parse_args()
    batch_predict(args.model_gcs_path, args.input_data_gcs_path, args.table_ref, args.project)


