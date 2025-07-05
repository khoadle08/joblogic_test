# --- Variables ---
TRAIN_IMAGE_NAME = acme-training
SERVE_IMAGE_NAME = acme-serving
KIND_CLUSTER_NAME = acme-cluster

.PHONY: all train deploy clean-all

# --- Main Targets ---
all: train deploy

# --- Part B: Training ---
# This target now correctly points to the 'training' subdirectory.
train:
	@echo "--- Building training Docker image from './training' directory... ---"
	docker build -t $(TRAIN_IMAGE_NAME):latest -f training/Dockerfile ./training
	@echo "--- Running training container... ---"
	mkdir -p ./data
	docker run --rm -v "$(PWD)/data:/app/output" $(TRAIN_IMAGE_NAME):latest
	@echo "--- Training complete. Updated model.pkl is in './data' directory. ---"

# --- Part C: Deployment ---
deploy: setup-kind build-api load-image-kind deploy-k8s
	@echo "--- Deployment Complete! ---"
	@echo "API is now accessible at http://localhost:5000"
	@echo "Try sending a POST request:"
	@echo "curl -X POST http://localhost:5000/predict -H 'Content-Type: application/json' -d '{\"job_type\":\"Plumbing\",\"job_priority\":\"High\",\"engineer_skill_level\":3,\"engineer_experience_years\":5,\"distance_km\":15.5}'"

# --- Helper Targets for Deployment ---
setup-kind:
	@if ! kind get clusters | grep -q "^$(KIND_CLUSTER_NAME)$$"; then \
		echo "--- Creating kind cluster '$(KIND_CLUSTER_NAME)' with port 5000 mapping... ---"; \
		kind create cluster --name $(KIND_CLUSTER_NAME) --config kind-config.yml; \
	else \
		echo "--- Kind cluster '$(KIND_CLUSTER_NAME)' already exists. ---"; \
	fi

build-api:
	@echo "--- Building API serving image... ---"
	# FIX: Create the target directory before copying the model file.
	mkdir -p ./app/model
	cp ./data/model.pkl ./app/model/
	docker build -t $(SERVE_IMAGE_NAME):latest ./app

load-image-kind:
	@echo "--- Loading serving image into kind cluster... ---"
	kind load docker-image $(SERVE_IMAGE_NAME):latest --name $(KIND_CLUSTER_NAME)

deploy-k8s:
	@echo "--- Applying Kubernetes manifests... ---"
	kubectl apply -f k8s/

# --- Cleanup Targets ---
clean-all:
	@echo "--- Deleting kind cluster... ---"
	kind delete cluster --name $(KIND_CLUSTER_NAME)
	@echo "--- Deleting Docker images... ---"
	docker rmi $(TRAIN_IMAGE_NAME):latest || true
	docker rmi $(SERVE_IMAGE_NAME):latest || true
	@echo "--- Deleting model data... ---"
	rm -rf ./data
	rm -rf ./app/model