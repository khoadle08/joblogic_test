# Makefile

# Define variables for image name
IMAGE_NAME = acme-training
TAG = latest

.PHONY: train clean

# Target to run the entire training workflow
train:
	@echo "--- Building training Docker image... ---"
	docker build -t $(IMAGE_NAME):$(TAG) .
	
	@echo "--- Running training container... ---"
	# Create data directory if it doesn't exist
	mkdir -p ./data
	# Run the container, mounting the local ./data directory to save the output model.
	# The volume mount is quoted to handle paths with spaces.
	docker run --rm -v "$(PWD)/data:/app/output" $(IMAGE_NAME):$(TAG)
	@echo "--- Training complete. Updated model.pkl is in ./data directory. ---"

# Optional: Target to clean up the created model and image
clean:
	@echo "--- Cleaning up... ---"
	rm -rf ./data/model.pkl
	docker rmi $(IMAGE_NAME):$(TAG) || true