
from config.config import base_image, project_id, region, serving_image
from kfp.v2 import dsl
from typing import NamedTuple
from kfp.v2.dsl import Model, Input

@dsl.component(base_image=base_image)
def deploy_model(
    optimal_model_name: str,
    project: str,
    region: str,
    serving_image: str,
    rf_model: Input[Model],
    dt_model: Input[Model],
) -> NamedTuple('Outputs', [('endpoint_name', str)]):
    """
    Deploy the optimal model to a Vertex AI endpoint.
    """
    # Import necessary libraries 
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
    }
    model_to_deploy = model_mapping[optimal_model_name]
    model_name = 'pet-adoption'

    logging.info(f"Model URI: {model_to_deploy.uri}")
    # Upload model to Vertex AI Model Registry
    model_upload = aiplatform.Model.upload(
        display_name=model_name,  
        artifact_uri=model_to_deploy.uri.rpartition('/')[0],
        serving_container_image_uri=serving_image,
        serving_container_health_route=f"/v1/models/{model_name}",  
        serving_container_predict_route=f"/v1/models/{model_name}:predict",  
        serving_container_environment_variables={"MODEL_NAME": model_name}  
    )

    logging.info(f"Model uploaded: {model_upload.resource_name}")

    # Create an endpoint
    endpoint = aiplatform.Endpoint.create(
        display_name=model_name,
        project=project,
        location=region
    )

    # Deploy model to the endpoint
    model_deployed = endpoint.deploy(
        model=model_upload,
        deployed_model_display_name=model_name,
        traffic_split={"0": 100},
        machine_type="n1-standard-4"
    )

    logging.info(f"Model deployed to endpoint: {endpoint.resource_name}")

    return (endpoint.resource_name,)
