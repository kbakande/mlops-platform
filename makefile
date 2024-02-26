.PHONY: help
help: ## Display this help screen
	@grep -h -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: all
all: run_pipeline run_inference_pipeline run_tests ## Run the ML pipeline, inference pipeline, and tests

.PHONY: run_pipeline
run_pipeline: ## Run the ML pipeline script
	@echo "Running ML pipeline..."
	python mlpipeline.py

.PHONY: run_inference_pipeline
run_inference_pipeline: ## Run the inference pipeline script
	@echo "Running inference pipeline..."
	python inference_pipeline.py

.PHONY: run_tests
run_tests: ## Run all tests in the tests/ directory
	@echo "Running tests..."
	pytest tests/

.PHONY: clean
clean: ## Clean up temporary files
	@echo "Cleaning up..."
	find . -type d -name '__pycache__' -exec rm -rf {} +
	find . -type f -name '*.pyc' -exec rm -f {} +
	find . -type f -name '*.pyo' -exec rm -f {} +
	find . -type f -name '*~' -exec rm -f {} +
	find . -type f -name '.pytest_cache' -exec rm -rf {} +
