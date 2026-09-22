from Ecommerce.exception.exception import EcommerceException
from Ecommerce.logging.logger import logging
from Ecommerce.constant.training_pipeline import training_pipeline
from Ecommerce.entity.config_entity import DataTransformataionConfig
from Ecommerce.entity.config_entity import DataIngestionConfig,DataValidationConfig
from Ecommerce.entity.artifact_entity import DataTransformationArtifact
from Ecommerce.entity.artifact_entity import DataValidationArtifact


from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer,KNNImputer
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import OneHotEncoder


import os
import sys
import pandas as pd
import numpy as np





class DataTransformation:
    def __init__(self,data_validation_artifact: DataValidationArtifact,
                data_transformation_config:DataTransformataionConfig):
        try:
            logging.info(f"Starting data tranformation")
            self.data_validation_artifact:DataValidationArtifact  = data_validation_artifact
            
            logging.info(f"-----------------------------------------------")
            self.data_transformation_config:DataTransformataionConfig = data_transformation_config
        except Exception as e:
            raise EcommerceException(e, sys)
        
    def get_preprocesser_object(self):
        try:
            numerical_columns = [
                "Age",
                "Quantity",
                "UnitPrice",
                "DiscountPct",
                "Rating",
                "ShippingDays",
                "DeliveryDistanceKM",
                "Spend90d",
                "Year",
                "Month",
                "Day"
            ]
            
            
            categorical_columns  = [

                'OrderDate', 
                'City',
                'Category',
                'ProductName',
                'PaymentMethod',
                'OrderStatus',
                'Device', 
                'MarketingChannel',
                'CouponCode'
            ]
            
            num_pipeline = Pipeline(
                steps=[
                    ("imputer", KNNImputer(
                    missing_values=np.nan,
                    n_neighbors=3,
                    weights="uniform"
                )),
                ("scaler", StandardScaler())
                ]
            )
            
            cat_pipeline = Pipeline(
                steps=[
                    ("imputed",SimpleImputer(strategy='most_frequent')),
                    ("oneHotEncoder",OneHotEncoder(handle_unknown="ignore"))
                ]
            )
            
            preprocessor = ColumnTransformer(
                transformers=[
                    ("numericalcolumns",num_pipeline,numerical_columns),
                    ("categoricalcolumns",cat_pipeline,categorical_columns)
                ]
            )
            
            
            return preprocessor
        except Exception as e:
            raise EcommerceException(e, sys)
    
    
    def initiate_data_transformation(self):
        try:
            train_df = pd.read_csv(
                self.data_validation_artifact.valid_train_file_path
            )
            
            test_df  = pd.read_csv(
                self.data_validation_artifact.valid_test_file_path
            )
            
            target = "TotalAmount"
            
            X_train = train_df.drop(columns=['TotalAmount', 'OrderId', 'CustomerId'])
            y_train = train_df['TotalAmount']

            X_test = test_df.drop(columns=['TotalAmount', 'OrderId', 'CustomerId'])
            y_test = test_df['TotalAmount']
            preprossoer_obj = self.get_preprocesser_object()
            
            X_trian_transformed = preprossoer_obj.fit_transform(X_train)
            X_test_transformed  = preprossoer_obj.transform(X_test)
            
            train_arr = np.c_[
                X_trian_transformed.toarray()
                if hasattr(X_trian_transformed, "toarray")
                else X_trian_transformed,
                y_train
            ]

            test_arr = np.c_[
                X_test_transformed.toarray()
                if hasattr(X_test_transformed, "toarray")
                else X_test_transformed,
                y_test
            ]
            
            os.makedirs(
                os.path.dirname(
                    self.data_transformation_config.transformed_train_file_path
                ),
                exist_ok=True
            )
            
            os.makedirs(
                os.path.dirname(
                    self.data_transformation_config.transformed_object_file_path
                ),
                exist_ok=True
            )
            
            np.save(
                self.data_transformation_config.transformed_train_file_path,
                train_arr
            )

            np.save(
                self.data_transformation_config.transformed_test_file_path,
                test_arr
            )
            
            import dill

            with open(
                self.data_transformation_config.transformed_object_file_path,
                "wb"
            ) as file:
                dill.dump(preprossoer_obj, file)

            data_transformation_artifact = DataTransformationArtifact(
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path,
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path
            )

            return data_transformation_artifact
            
        except Exception as e:
            raise EcommerceException(e, sys)
        