# app/Dockerfile

# Use a slim, secure base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code and the trained model
COPY main.py .
# The model from the training step should be placed in app/model/
COPY ./model/model.pkl ./model/

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application using uvicorn
# 0.0.0.0 is necessary to accept connections from outside the container
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
