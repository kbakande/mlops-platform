import pytest
from kfp.v2 import compiler
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from mlpipeline import mlplatform_pipeline

def test_pipeline_compiles():
    """
    Test if the ML pipeline compiles without errors.
    """

    compiler.Compiler().compile(pipeline_func=mlplatform_pipeline, package_path="tmp_pipeline.json")

    assert os.path.exists("tmp_pipeline.json")

    os.remove("tmp_pipeline.json")
