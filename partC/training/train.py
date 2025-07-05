# train.py

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
import pickle
import os

# Define paths
DATA_FILE_PATH = 'sample_data.csv'
MODEL_OUTPUT_DIR = '/app/output'
MODEL_FILE_PATH = os.path.join(MODEL_OUTPUT_DIR, 'model.pkl')

print("Starting training process...")

# Load the dataset from the provided CSV file [cite: 1]
try:
    df = pd.read_csv(DATA_FILE_PATH)
    print(f"Dataset loaded successfully. Shape: {df.shape}")
except FileNotFoundError:
    print(f"Error: {DATA_FILE_PATH} not found.")
    exit(1)

# Define features and target
# 'success' is the target variable indicating job success [cite: 1]
target = 'success'
# Features include job type, priority, and engineer's qualifications [cite: 1]
features = ['job_type', 'job_priority', 'engineer_skill_level', 'engineer_experience_years', 'distance_km']
categorical_features = ['job_type', 'job_priority']
numerical_features = ['engineer_skill_level', 'engineer_experience_years', 'distance_km']

X = df[features]
y = df[target]

# Create pre-processing pipelines for numerical and categorical data
# Numerical features will be scaled
numerical_transformer = StandardScaler()

# Categorical features will be one-hot encoded
categorical_transformer = OneHotEncoder(handle_unknown='ignore')

# Create a preprocessor object using ColumnTransformer
preprocessor = ColumnTransformer(
    transformers=[
        ('num', numerical_transformer, numerical_features),
        ('cat', categorical_transformer, categorical_features)
    ])

# Create the full model pipeline
# The model is a Gradient Boosting Classifier as specified 
model_pipeline = Pipeline(steps=[('preprocessor', preprocessor),
                                 ('classifier', GradientBoostingClassifier(n_estimators=100, random_state=42))])

# Train the model
print("Training the model...")
model_pipeline.fit(X, y)
print("Model training completed.")

# Ensure the output directory exists
os.makedirs(MODEL_OUTPUT_DIR, exist_ok=True)

# Save the trained pipeline to model.pkl
print(f"Saving model to {MODEL_FILE_PATH}...")
with open(MODEL_FILE_PATH, 'wb') as f:
    pickle.dump(model_pipeline, f)

print("Training script finished successfully.")