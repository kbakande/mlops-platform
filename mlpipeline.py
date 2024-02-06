from kfp.v2 import dsl, compiler
from kfp.v2.dsl import pipeline
from components.load_data import load_data
from components.preprocess_data import preprocess_data
from components.train_random_forest import train_random_forest
from components.train_decision_tree import train_decision_tree
from components.evaluate_model import evaluate_model
from components.deploy_model import deploy_model
from config.config import gcs_url, train_ratio, project_id, region, serving_image, service_account, pipeline_root

@pipeline(
    name="ml-platform-pipeline",
    description="A pipeline that performs data loading, preprocessing, model training, evaluation, and deployment",
    pipeline_root= pipeline_root
)
def mlplatform_pipeline(
    gcs_url: str = gcs_url,
    train_ratio: float = train_ratio,
    ):
    load_data_op = load_data(gcs_url=gcs_url)
    preprocess_data_op = preprocess_data(input_dataset=load_data_op.output, 
                                         train_ratio=train_ratio
                                         )

    train_rf_op = train_random_forest(train_dataset=preprocess_data_op.outputs['train_dataset'])
    train_dt_op = train_decision_tree(train_dataset=preprocess_data_op.outputs['train_dataset'])

    evaluate_op = evaluate_model(
        test_dataset=preprocess_data_op.outputs['test_dataset'],
        dt_model=train_dt_op.output,
        rf_model=train_rf_op.output
    )

    deploy_model_op = deploy_model(
        optimal_model_name=evaluate_op.outputs['optimal_model'],
        project=project_id,
        region=region,
        serving_image=serving_image,
        rf_model=train_rf_op.output,
        dt_model=train_dt_op.output
    )

if __name__ == "__main__":
    # Compiling the pipeline
    pipeline_filename = "mlplatform_pipeline.json"
    compiler.Compiler().compile(
        pipeline_func=mlplatform_pipeline,
        package_path=pipeline_filename
    )

    # Deploying the pipeline to Vertex AI
    from google.cloud import aiplatform
    aiplatform.init(project=project_id, location=region)
    _ = aiplatform.PipelineJob(
        display_name="ml-platform-pipeline",
        template_path=pipeline_filename,
        parameter_values={
            "gcs_url": gcs_url,
            "train_ratio": train_ratio
        },
        enable_caching=True
    ).submit(service_account=service_account)