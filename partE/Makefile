# --- Variables ---
TRAIN_IMAGE_NAME = acme-training
SERVE_IMAGE_NAME = acme-serving
KIND_CLUSTER_NAME = acme-cluster

.PHONY: all train deploy clean-all monitor clean-monitor airflow-up airflow-down


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

# --- Part D: Monitoring ---
monitor:
	@echo "--- Building API image for monitoring stack... ---"
	# Đảm bảo mô hình đã được sao chép
	mkdir -p ./app/model
	cp ./data/model.pkl ./app/model/
	@echo "--- Starting Monitoring Stack (Prometheus + Grafana)... ---"
	# FIX: Thêm dấu ngoặc kép vào "$(PWD)" để xử lý đúng các đường dẫn có khoảng trắng.
	export PWD="$(PWD)" && docker-compose -f monitoring/docker-compose.monitoring.yml up -d --build
	@echo "--- Monitoring Stack is UP! ---"
	@echo "Grafana: http://localhost:3000 (user: admin, pass: admin)"
	@echo "Prometheus: http://localhost:9090"
	@echo "API (for testing): http://localhost:8000"

# --- Cleanup Targets ---
clean-monitor:
	@echo "--- Stopping Monitoring Stack... ---"
	export PWD="$(PWD)" && docker-compose -f monitoring/docker-compose.monitoring.yml down -v


# --- Part E: Airflow Data Pipeline ---
airflow-up:
	@echo "--- Starting Airflow Environment... ---"
	# Set the Airflow UID to the current user to avoid permission errors
	echo "AIRFLOW_UID=$$(id -u)" > .env
	# FIX: Add quotes around PWD to handle paths with spaces
	export PWD="$(PWD)" && docker-compose -f docker-compose.airflow.yml up -d --build
	@echo "--- Airflow is starting up! ---"
	@echo "Access the UI at: http://localhost:8080 (user: airflow, pass: airflow)"

airflow-down:
	@echo "--- Stopping Airflow Environment... ---"
	# FIX: Add quotes around PWD to handle paths with spaces
	export PWD="$(PWD)" && docker-compose -f docker-compose.airflow.yml down -v
	rm -f .env

# --- NEW: Debugging Target for Airflow ---
airflow-debug:
	@echo "--- Starting Airflow in DEBUG mode... ---"
	@echo "--- Logs will be displayed below. Press Ctrl+C to stop. ---"
	# Set the Airflow UID to the current user to avoid permission errors
	echo "AIRFLOW_UID=$$(id -u)" > .env
	# Run without the '-d' flag to see logs in the terminal
	export PWD="$(PWD)" && docker-compose -f docker-compose.airflow.yml up --build

# --- Cleanup Targets ---
clean-all:
	@echo "--- Deleting kind cluster... ---"
	kind delete cluster --name $(KIND_CLUSTER_NAME) || true
	@echo "--- Stopping monitoring stack... ---"
	export PWD="$(PWD)" && docker-compose -f monitoring/docker-compose.monitoring.yml down -v || true
	@echo "--- Stopping Airflow environment... ---"
	export PWD="$(PWD)" && docker-compose -f docker-compose.airflow.yml down -v || true
	@echo "--- Deleting Docker images... ---"
	docker rmi $(TRAIN_IMAGE_NAME):latest || true
	docker rmi $(SERVE_IMAGE_NAME):latest || true
	@echo "--- Deleting model data... ---"
	rm -rf ./data
	rm -rf ./app/model
	rm -f .env
