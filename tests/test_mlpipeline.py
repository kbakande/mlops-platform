import pytest
from kfp.v2 import compiler
import os
import sys

# Add the project root to the PYTHONPATH for importing mlpipeline
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from mlpipeline import mlplatform_pipeline

def test_pipeline_compiles():
    """
    Test if the ML pipeline compiles without errors.
    """
    # Compile the pipeline to a temporary JSON file
    compiler.Compiler().compile(pipeline_func=mlplatform_pipeline, package_path="tmp_pipeline.json")

    # Assert the pipeline JSON file is created
    assert os.path.exists("tmp_pipeline.json")

    # Clean up - remove the temporary file after test
    os.remove("tmp_pipeline.json")
