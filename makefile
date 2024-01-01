# Default target
all: run_pipeline run_tests

# Run the ML pipeline
run_pipeline:
	@echo "Running ML pipeline..."
	python mlpipeline.py

# Run tests
run_tests:
	@echo "Running tests..."
	pytest tests/

# Clean up temporary files
clean:
	@echo "Cleaning up..."
	find . -type d -name '__pycache__' -exec rm -rf {} +
	find . -type f -name '*.pyc' -exec rm -f {} +
	find . -type f -name '*.pyo' -exec rm -f {} +
	find . -type f -name '*~' -exec rm -f {} +
	find . -type f -name '.pytest_cache' -exec rm -rf {} +

# Display help information
help:
	@echo "Makefile commands:"
	@echo "all            - Run the ML pipeline and tests"
	@echo "run_pipeline   - Run the ML pipeline script"
	@echo "run_tests      - Run all tests in the tests/ directory"
	@echo "clean          - Clean up temporary files"
	@echo "help           - Display this help information"
