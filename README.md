# MLPlatform: Machine Learning Pipeline on GCP
`MLPlatform` is a robust machine learning pipeline designed to streamline ML workflows on Google Cloud Platform (GCP) resources. Following best practices in MLOps and DevOps, it offers a structured and efficient approach to managing data loading, preprocessing, model training, evaluation, and deployment.

## Pipeline Visualization

Below is a visualization of the MLPlatform pipeline components as executed on Vertex AI:

![MLPlatform Pipeline on Vertex AI](images/mlpipeline.png)

The diagram illustrates the sequential and parallel processing of tasks within the pipeline:

- `load-data`: Fetches and loads data into the pipeline.
- `preprocess-data`: Processes the loaded data, preparing it for training.
- `train-decision-tree` and `train-random-frost`: Train two separate models in parallel.
- `evaluate-model`: Evaluates both models and selects the best performing one.
- `deploy-model`: Deploys the chosen model to a Vertex AI endpoint for serving.

Each component runs in a containerized environment, ensuring isolation and scalability.
## Project Structure

```graphql
mlplatform_project/
│
├── components/               # Pipeline components (data load, preprocess, train, etc.)
│   ├── load_data.py
│   ├── preprocess_data.py
│   ├── train_decision_tree.py
│   ├── train_random_forest.py
│   ├── evaluate_model.py
│   └── deploy_model.py
│
├── config/                   # Configuration files and settings
│   ├── __init__.py
│   └── config.py
│
├── notebooks/                # Jupyter notebooks for demonstrations and experiments
│   └── mlplatform.ipynb
│
├── tests/                    # Test scripts for pipeline components
│   └── test_mlpipeline.py
│
├── mlpipeline.py             # Main pipeline script
├── pyproject.toml            # Project dependencies and configurations
├── poetry.lock               # Poetry lock file for dependencies management
├── Makefile                  # Makefile for easy execution of tasks
└── README.md                 # Project overview and documentation
```
## Installation

1. Clone the Repository:

   Clone the `mlplatform` repository to your local machine.

 ```bash
 git clone git@github.com:kbakande/MLOPS.git
 cd mlplatform_project
 ```

2. Install Python:

   Ensure you have Python >= 3.9 installed. You can download it from [python.org](https://www.python.org/).

3. Install Dependencies:

   Use [Poetry](https://python-poetry.org/) for managing Python dependencies:

   ```bash
   poetry install
   ```

## Usage
    The project includes a Makefile for easy execution of tasks:

* Run the ML Pipeline:

```bash
make run_pipeline
```

* Run Tests:

```bash
make run_tests
```

* Clean Temporary Files:

```bash
make clean
```

* Display Help Information:

```bash
make help
```

## Dependencies

    Key Python libraries and frameworks used in this project:

* Pandas
* NumPy
* Scikit-learn
* XGBoost
* LightGBM
* Google Cloud AI Platform
* Pytest for testing
* Kubeflow Pipelines (KFP)

## Author
[Kabeer Akande](https://www.linkedin.com/in/koakande/)
