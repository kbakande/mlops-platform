
import os
from dotenv import load_dotenv

load_dotenv()

pipeline_root = os.environ['PIPELINE_ROOT']
base_image = os.environ.get("CONTAINER_IMAGE")
serving_image = os.environ.get("SERVING_IMAGE")
project_id = os.environ['PROJECT_ID']
region = os.environ['REGION']
service_account = os.environ['SERVICE_ACCOUNT']
artifact_repo = os.environ['ARTIFACT_REPO']
gcs_url = os.environ['GCS_URL']
train_ratio = float(os.environ['TRAIN_RATIO'])
bucket_name = os.environ['BUCKET_NAME']
model_gcs_path = os.environ['MODEL_GCS_PATH'] 
input_data_gcs_path = os.environ['GCS_URL'] 
table_ref = os.environ['TABLE_REF']
