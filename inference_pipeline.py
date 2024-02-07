from kfp import dsl, compiler
from kfp.dsl import pipeline
from batch_prediction.batch_predict import batch_predict
from config.config import model_gcs_path, input_data_gcs_path, table_ref, \
    project_id, region, pipeline_root, service_account

@pipeline(
    name="inference_pipeline",
    description="A pipeline that returns predictions from deployed model",
    pipeline_root= pipeline_root
)
def inference_pipeline(
    model_gcs_path: str = model_gcs_path,
    input_data_gcs_path: str = input_data_gcs_path,  
    table_ref:str = table_ref, 
    project: str = project_id                      
    ):
    
    batch_prediction_op = batch_predict(model_gcs_path=model_gcs_path,
                                        input_data_gcs_path=input_data_gcs_path,
                                        table_ref=table_ref, 
                                        project=project
                                        )

if __name__ == "__main__":
    # Compiling the pipeline
    pipeline_filename = "inference_pipeline.json"
    compiler.Compiler().compile(
        pipeline_func=inference_pipeline,
        package_path=pipeline_filename
    )

    # Deploying the pipeline to Vertex AI
    from google.cloud import aiplatform
    aiplatform.init(project=project_id, location=region)
    _ = aiplatform.PipelineJob(
        display_name="inference-pipeline",
        template_path=pipeline_filename,
        parameter_values={
            "model_gcs_path": model_gcs_path,
            "input_data_gcs_path": input_data_gcs_path,  
            "table_ref": table_ref, 
            "project": project_id  
        },
        enable_caching=False
    ).submit(service_account=service_account)