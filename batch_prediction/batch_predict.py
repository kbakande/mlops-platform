
def batch_predict(model_gcs_path: str,
                  input_data_gcs_path:str,
                  project: str,
                  target_column = None):
   """
   Loads data form GCS, obtain predictions and write data to BQ
   """
    # Import libraries
    from google.cloud import storage, bigquery
    import pandas as pd
    import joblib
    import os

    # Load model from GCS
    storage_client = storage.Client()
    bucket_name, model_path = model_gcs_path.replace("gs://", "").split("/", 1)
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(model_path)
    model_filename = "/tmp/model.joblib"
    blob.download_to_filename(model_filename)
    model = joblib.load(model_filename)

    # Load input data for prediction
    _, input_data_path = input_data_gcs_path.replace("gs://", "").split("/", 1)
    blob = bucket.blob(input_data_path)
    input_data_filename = "/tmp/input_data.csv"
    blob.download_to_filename(input_data_filename)
    input_data = pd.read_csv(input_data_filename).sample(10)

    # Preprocess input data
    if target_column:
        input_data.drop(columns=[target_column], inplace=True, errors='ignore')
    else:
      input_data = input_data[:, :-1]

    # Convert categorical columns to 'category' data type
    categorical_cols = input_data.select_dtypes(include=['object']).columns
    input_data[categorical_cols] = input_data[categorical_cols].astype('category')

    # Make predictions
    predictions = model.predict(input_data)

    # Write predictions to BigQuery
    bigquery_client = bigquery.Client(project=project)
    table_ref = table_ref
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
    job.result()  # Wait for the job to complete

    return (f"Predictions written to {table_ref}",)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Obtain batch prediction from Vertex AI model')

    parser.add_argument('--model_gcs_path', required=True, help='Model GCS path')
    parser.add_argument('--input_data_gcs_path', required=True, help='Input data GCS path')
    parser.add_argument('--project', required=True, help='GCP project name')

    args = parser.parse_args()
    
    batch_predict(args)
