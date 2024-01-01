# components/deploy_model.py
from config.config import base_image, project_id, region, serving_image
from kfp.v2 import dsl
from typing import NamedTuple
from kfp.v2.dsl import Model, Input

@dsl.component(base_image=base_image)
def deploy_model(
    optimal_model_name: str,
    project: str = project_id,
    region: str = region,
    serving_image: str = serving_image,
    rf_model: Input[Model],
    dt_model: Input[Model],
) -> NamedTuple('Outputs', [('model_resource_name', str)]):
    """
    Deploy the optimal model to a Vertex AI endpoint.
    """
    # Import necessary libraries within the function
    from google.cloud import aiplatform
    import logging

    # Set up logging
    logging.basicConfig(level=logging.INFO)

    # Initialize the AI Platform client
    aiplatform.init(project=project, location=region)

    # Select the optimal model based on the name
    model_mapping = {
        "decision_tree": dt_model,
        "random_forest": rf_model,
        # Map additional models if necessary
    }
    model_to_deploy = model_mapping[optimal_model_name]

    # Upload model to Vertex AI Model Registry
    model_upload = aiplatform.Model.upload(
        display_name="your-model-display-name",  # Customize as needed
        artifact_uri=model_to_deploy.uri.rpartition('/')[0],
        serving_container_image_uri=serving_image,
        serving_container_health_route="/v1/models/your-model-name",  # Customize as needed
        serving_container_predict_route="/v1/models/your-model-name:predict",  # Customize as needed
        serving_container_environment_variables={"MODEL_NAME": "your-model-name"}  # Customize as needed
    )

    logging.info(f"Model uploaded: {model_upload.resource_name}")

    return (model_upload.resource_name,)
