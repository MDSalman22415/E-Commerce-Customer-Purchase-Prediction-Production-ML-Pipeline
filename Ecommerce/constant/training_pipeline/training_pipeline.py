import os
import sys
import numpy as np

"""
defining common constant variable for training pipeline
"""

TARGET_COLUMN = "total_amount"
PIPELINE_NAME : str = "Ecommerce"
ARTIFACT_DIR  : str = "Artifact"
FILE_NAME     : str = "Cleaned_data.csv"

TRAIN_FILE_NAME : str = "train.csv"
TEST_FILE_NAME  : str = "test.csv"

SCHEMA_FILE_PATH  = os.path.join("data_schema","schema.yaml")



SAVED_MODEL_DIR  = os.path.join("save_model")
MODEL_FILE_NAME  =  "model.pkl"

"""
STARTING DATAINGSTION 
"""
DATA_INGESTION_COLLECTION_NAME : str  = "Ecommercedata"
DATA_INGESTION_DATABASE_NAME   : str  = "Ecommerce"
DATA_INGESTION_DIR_NAME        : str  = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR : str = "ingested"
DATA_INGESTION_INGESTED_DIR      : str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATION : str = 0.2



"""
Data Validation constant
"""
DATA_VALIDATION_DIR_NAME : str = "data_validation"
DATA_VALIDATION_VALID_DIR: str = "validated"
DATA_VALIDATION_INVALID_DIR : str = "invalid"
DATA_VALIDATION_DRIFT_REPORT_DIR : str  = "drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME : str = "report.yaml"