from Ecommerce.exception.exception import EcommerceException
from Ecommerce.logging.logger import logging
from Ecommerce.entity.config_entity import DataIngestionConfig
from Ecommerce.entity.config_entity import DataValidationConfig
from Ecommerce.entity.artifact_entity import DataValidationArtifact
from Ecommerce.entity.artifact_entity import DataIngestionArtifact
from Ecommerce.entity.config_entity import TrainingPipelineConfig
from Ecommerce.constant.training_pipeline.training_pipeline import SCHEMA_FILE_PATH

from Ecommerce.utils.main.utlis import read_yaml_file, write_ymal_file

import os
import pandas as pd
import numpy as np
import sys

from scipy.stats import ks_2samp


class DataValidation:

    def __init__(
        self,
        data_ingestion_artifact: DataIngestionArtifact,
        data_validation_config: DataValidationConfig
    ):
        try:
            logging.info("Data Validation is starting....")

            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config

            self.__schema_config = read_yaml_file(
                SCHEMA_FILE_PATH
            )

        except Exception as e:
            raise EcommerceException(e, sys)

    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)

        except Exception as e:
            raise EcommerceException(e, sys)

    def validate_number_of_columns(
        self,
        dataframe: pd.DataFrame
    ):
        try:
            number_of_columns = len(self.__schema_config)

            logging.info(
                f"Number of columns: {number_of_columns}"
            )

            logging.info(
                f"Number of columns in dataframe: "
                f"{len(dataframe.columns)}"
            )

            if len(dataframe.columns) == number_of_columns:
                return True

            return False

        except Exception as e:
            raise EcommerceException(e, sys)

    def validate_number_of_numerical_columns(
        self,
        dataframe: pd.DataFrame
    ):
        try:
            number_of_numerical_columns = len(
                self.__schema_config["numerical_columns"]
            )

            logging.info(
                f"Reading Numerical columns to validating: "
                f"{number_of_numerical_columns}"
            )

            dataframe_of_numerical_columns = len(
                dataframe.select_dtypes(
                    include=["int64", "float64"]
                ).columns
            )

            logging.info(
                f"Reading columns in dataframe: "
                f"{dataframe_of_numerical_columns}"
            )

            if (
                number_of_numerical_columns
                == dataframe_of_numerical_columns
            ):
                return True

            return False

        except Exception as e:
            raise EcommerceException(e, sys)

    def detect_dataset_drift(
        self,
        base_df,
        current_df,
        threshold=0.05
    ) -> bool:

        try:
            status = True
            report = {}

            # Only numerical columns
            numerical_columns = base_df.select_dtypes(
                include=["int64", "float64"]
            ).columns

            for column in numerical_columns:

                d1 = base_df[column]
                d2 = current_df[column]

                is_same_dist = ks_2samp(d1, d2)

                if threshold <= is_same_dist.pvalue:
                    is_found = False

                else:
                    is_found = True
                    status = False

                report.update({
                    column: {
                        "p_value": float(
                            is_same_dist.pvalue
                        ),
                        "drift_status": is_found
                    }
                })

            drift_report_file_path = (
                self.data_validation_config.drift_report_file_path
            )

            dir_path = os.path.dirname(
                drift_report_file_path
            )

            os.makedirs(
                dir_path,
                exist_ok=True
            )

            write_ymal_file(
                file_path=drift_report_file_path,
                content=report
            )

            return status

        except Exception as e:
            raise EcommerceException(e, sys)

    def initaite_data_validation(
        self
    ) -> DataValidationArtifact:

        try:
            error_message = ""

            train_file_path = (
                self.data_ingestion_artifact.train_file_path
            )

            test_file_path = (
                self.data_ingestion_artifact.test_file_path
            )

            # Read data from train and test
            train_dataframe = DataValidation.read_data(
                train_file_path
            )

            test_dataframe = DataValidation.read_data(
                test_file_path
            )

            # Validate number of columns
            status = self.validate_number_of_columns(
                dataframe=train_dataframe
            )

            if not status:
                error_message = (
                    f"{error_message}"
                    f"Train dataframe does not contain all columns"
                )

            status = self.validate_number_of_columns(
                dataframe=test_dataframe
            )

            if not status:
                error_message = (
                    f"{error_message}"
                    f"Test dataframe does not contain all columns"
                )

            # Validate numerical columns
            status_two = self.validate_number_of_numerical_columns(
                dataframe=train_dataframe
            )

            if not status_two:
                error_message = (
                    f"{error_message}"
                    f"Train dataset does not contain all numerical columns"
                )

            status_two = self.validate_number_of_numerical_columns(
                dataframe=test_dataframe
            )

            if not status_two:
                error_message = (
                    f"{error_message}"
                    f"Test dataset does not contain all numerical columns"
                )

            # Check dataset drift
            status = self.detect_dataset_drift(
                base_df=train_dataframe,
                current_df=test_dataframe
            )

            # Create directory
            dir_path = os.path.dirname(
                self.data_validation_config.valid_train_file_path
            )

            os.makedirs(
                dir_path,
                exist_ok=True
            )

            # Save valid train data
            train_dataframe.to_csv(
                self.data_validation_config.valid_train_file_path,
                index=False,
                header=True
            )

            # Save valid test data
            test_dataframe.to_csv(
                self.data_validation_config.vlaid_test_file_path,
                index=False,
                header=True
            )

            # Create validation artifact
            self.validation_artifact = DataValidationArtifact(
                validation_status=status,

                valid_train_file_path=(
                    self.data_validation_config.valid_train_file_path
                ),

                valid_test_file_path=(
                    self.data_validation_config.vlaid_test_file_path
                ),

                invalid_train_file_path=None,

                invalid_test_file_path=None,

                drift_report_file_path=(
                    self.data_validation_config.drift_report_file_path
                )
            )

            return self.validation_artifact

        except Exception as e:
            raise EcommerceException(e, sys)