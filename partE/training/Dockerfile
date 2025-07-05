# Dockerfile

# --- Stage 1: Builder ---
# Use a slim Python image as the base for building dependencies
FROM python:3.9-slim as builder

# Set the working directory
WORKDIR /app

# Install build dependencies that might be needed for some Python packages
RUN apt-get update && apt-get install -y --no-install-recommends gcc build-essential

# Copy only the requirements file first to leverage Docker cache
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt


# --- Stage 2: Final Image ---
# Start from a fresh slim Python image for the final, smaller image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the installed packages from the builder stage
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages

# Copy the training script and the data file into the final image
COPY train.py .
COPY sample_data.csv .

# Set the command to run when the container starts
# This executes the training script 
CMD ["python", "train.py"]