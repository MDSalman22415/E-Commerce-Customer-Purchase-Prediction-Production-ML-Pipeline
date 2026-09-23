
import os
import sys
from Ecommerce.entity.artifact_entity import (
    ModelTrainerArtifact,
    DataTransformationArtifact,
    RegressionMetricArtifact,
)
import numpy as np
from Ecommerce.exception.exception import EcommerceException
from Ecommerce.logging.logger import logging

from Ecommerce.entity.artifact_entity import (
    ModelTrainerArtifact,
    DataTransformationArtifact,
)
from Ecommerce.entity.config_entity import ModelTrainerConfig

from Ecommerce.utils.main.utlis import evaluate_metirc,save_obj,load_numpy_array_data,load_object

from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import Ridge, Lasso, ElasticNet
from sklearn.ensemble import RandomForestRegressor, AdaBoostRegressor

from sklearn.metrics import r2_score


class ModelTrainer:

    def __init__(
        self,
        data_transformation_artifact: DataTransformationArtifact,
        model_trainer_config: ModelTrainerConfig,
    ):
        try:
            logging.info("Model Trainer Starting...")

            self.data_transformation_artifact = data_transformation_artifact
            self.model_trainer_config = model_trainer_config

        except Exception as e:
            raise EcommerceException(e, sys)

    def train_model(self, X_train, y_train, X_test, y_test):

        try:

            logging.info("Defining models")

            models = {
                "Decision Tree": DecisionTreeRegressor(),
                "Ridge": Ridge(),
                "Lasso": Lasso(),
                "Elastic Net": ElasticNet(),
                "Random Forest": RandomForestRegressor(),
                "AdaBoost": AdaBoostRegressor(),
            }

            params = {
                "Decision Tree": {
                    "max_depth": [5, 10],
                },

                "Ridge": {
                    "alpha": [0.1, 1.0],
                },

                "Lasso": {
                    "alpha": [0.01, 0.1],
                },

                "Elastic Net": {
                    "alpha": [0.01, 0.1],
                    "l1_ratio": [0.5],
                },

                "Random Forest": {
                    "n_estimators": [50, 100],
                    "max_depth": [5, 10],
                },

                "AdaBoost": {
                    "n_estimators": [50, 100],
                    "learning_rate": [0.1],
                },
            }

            model_report = evaluate_metirc(
                X_train=X_train,
                y_train=y_train,
                X_test=X_test,
                y_test=y_test,
                models=models,
                parms=params,
            )

            # Get best model score
            best_model_score = max(model_report.values())

            # Get best model name
            best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]

            # Get best model
            best_model = models[best_model_name]

            # Train best model
            best_model.fit(X_train, y_train)

            # Prediction
            y_train_pred = best_model.predict(X_train)
            y_test_pred = best_model.predict(X_test)

            # Calculate R2 score
            train_model_score = r2_score(y_train, y_train_pred)
            test_model_score = r2_score(y_test, y_test_pred)

            logging.info(
                f"Best Model: {best_model_name}"
            )

            logging.info(
                f"Train R2 Score: {train_model_score}"
            )

            logging.info(
                f"Test R2 Score: {test_model_score}"
            )

            return best_model

        except Exception as e:
            raise EcommerceException(e, sys)

    def initiate_model_trainer(self) -> ModelTrainerArtifact:

        try:

            train_file_path = (
                self.data_transformation_artifact.transformed_train_file_path
            )

            test_file_path = (
                self.data_transformation_artifact.transformed_test_file_path
            )

            # Load transformed data
            train_arr = load_numpy_array_data(train_file_path)
            test_arr = load_numpy_array_data(test_file_path)
            
            
            # Separate X and y
            X_train = train_arr[:, :-1]
            y_train = train_arr[:, -1]

            X_test = test_arr[:, :-1]
            y_test = test_arr[:, -1]
            print("X_train shape:", X_train.shape)
            print("y_train shape:", y_train.shape)
            print("NaN in y_train:", np.isnan(y_train).sum())
            # Train model
            best_model = self.train_model(
                X_train,
                y_train,
                X_test,
                y_test,
            )

            # Save model
            model_dir_path = os.path.dirname(
                self.model_trainer_config.trained_model_file_path
            )

            os.makedirs(model_dir_path, exist_ok=True)

            save_obj(
                self.model_trainer_config.trained_model_file_path,
                best_model,
            )

            # Create artifact
            model_trainer_artifact = ModelTrainerArtifact(
                trained_model_file_path=self.model_trainer_config.trained_model_file_path,
                train_metric_artifact=train_model_score,
                test_metric_artifact=test_model_score,
            )
            print("y_train NaN:", np.isnan(y_train).sum())
            print("y_test NaN:", np.isnan(y_test).sum())

            return model_trainer_artifact

        except Exception as e:
            raise EcommerceException(e, sys)

