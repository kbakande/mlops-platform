import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

pipeline_root = os.environ['PIPELINE_ROOT']
base_image = os.environ.get("CONTAINER_IMAGE")
serving_image = os.environ.get("SERVING_IMAGE")
project_id = os.environ['PROJECT_ID']
region = os.environ['REGION']
service_account = os.environ['SERVICE_ACCOUNT']
artifact_repo = os.environ['ARTIFACT_REPO']
model_display_name = os.environ['MODEL_DISPLAY_NAME']
model_name = os.environ['MODEL_NAME']
endpoint_name = os.environ['ENDPOINT_NAME']
gcs_url = os.environ['GCS_URL']
train_ratio = float(os.environ['TRAIN_RATIO'])
bucket_name = os.environ['BUCKET_NAME']
