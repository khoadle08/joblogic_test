# airflow/dags/data_pipeline_dag.py
from __future__ import annotations

import pendulum
import pandas as pd
from pathlib import Path

from airflow.decorators import dag, task

# Define paths relative to the Airflow home directory inside the container
AIRFLOW_HOME = Path('/opt/airflow')
INPUT_DATA_PATH = AIRFLOW_HOME / 'sample_data.csv'
OUTPUT_DIR = AIRFLOW_HOME / 'data' / 'raw'
OUTPUT_FILE_PATH = OUTPUT_DIR / 'transformed_job_data.csv'

@dag(
    dag_id='job_data_etl_pipeline',
    schedule=None, # This DAG will be triggered manually
    start_date=pendulum.datetime(2025, 7, 5, tz="UTC"),
    catchup=False,
    tags=['mlops-assessment', 'etl'],
    doc_md="""
    ### Job Data ETL Pipeline

    This DAG performs a simple ETL process on job data.
    1.  **Extract**: Reads the raw data from `sample_data.csv`.
    2.  **Transform**: Adds a new 'experience_level' column.
    3.  **Load**: Saves the transformed data to the `/data/raw/` directory.
    """
)
def job_data_etl_pipeline():
    """
    This pipeline extracts job data, performs a simple transformation,
    and loads it into a target directory.
    """
    @task
    def fetch_data() -> str:
        """Reads the source CSV file and returns its content as a string."""
        print(f"Fetching data from: {INPUT_DATA_PATH}")
        if not INPUT_DATA_PATH.exists():
            raise FileNotFoundError(f"Input data file not found at {INPUT_DATA_PATH}")
        
        df = pd.read_csv(INPUT_DATA_PATH)
        # Pass data to the next task via XComs by returning its JSON representation
        return df.to_json()

    @task
    def transform_data(data_json: str) -> str:
        """
        Performs a simple transformation on the data.
        - Adds an 'experience_level' column based on experience years.
        """
        print("Transforming data...")
        df = pd.read_json(data_json)

        def get_experience_level(years):
            if years < 3:
                return 'Junior'
            elif 3 <= years < 10:
                return 'Mid-level'
            else:
                return 'Senior'

        df['experience_level'] = df['engineer_experience_years'].apply(get_experience_level)
        print("Added 'experience_level' column.")
        print(df.head())
        
        return df.to_json()

    @task
    def load_data(transformed_data_json: str):
        """Saves the transformed data to a new CSV file."""
        print(f"Saving transformed data to: {OUTPUT_FILE_PATH}")
        df = pd.read_json(transformed_data_json)
        
        # Ensure the output directory exists
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        
        df.to_csv(OUTPUT_FILE_PATH, index=False)
        print(f"Successfully saved {len(df)} rows to {OUTPUT_FILE_PATH}")

    # Define the task dependencies
    raw_data = fetch_data()
    transformed_data = transform_data(raw_data)
    load_data(transformed_data)

# Instantiate the DAG
job_data_etl_pipeline()
