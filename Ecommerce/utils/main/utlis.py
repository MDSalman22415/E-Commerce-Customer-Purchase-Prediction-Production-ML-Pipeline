import yaml
from Ecommerce.exception.exception import EcommerceException
from Ecommerce.logging.logger import logging
from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV
import os
import sys
import pickle
import numpy as np
import pandas as pd



def read_yaml_file(file_path :str) -> dict:
    try:
        with open(file_path, "rb") as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise EcommerceException(e, sys)

def write_ymal_file(
        file_path: str,
        content: object,
        replace: bool = False
) -> None:
    try:
        if replace and os.path.exists(file_path):
            os.remove(file_path)

        os.makedirs(
            os.path.dirname(file_path),
            exist_ok=True
        )

        with open(file_path, "w") as file:
            yaml.dump(content, file)

    except Exception as e:
        raise EcommerceException(e, sys)
    

def evaluate_metirc(X_train,y_train,X_test,y_test,models,parms):
    try:
        logging.info("Starting a evaluting metirx")
        report = {}
        
        for i in range (len(list(models))):
            model  = list(models.values())[i]
            para   = parms[list(models.keys())[i]]
            
            # gs = GridSearchCV(model,para,cv=3)
            # gs.fit(X_train,y_train)
            
            # model.set_params(**gs.best_params_)
            
            model.fit(X_train,y_train)
            
            y_train_pred = model.predict(X_train)
            
            y_test_pred  = model.predict(X_test)
            
            train_model_score  = r2_score(y_train,y_train_pred)
            
            test_model_score   = r2_score(y_test,y_test_pred)
            
            report[list(models.keys())[i]] = test_model_score
        return report
    except Exception as e:
        raise EcommerceException(e, sys)


def save_obj(file_path :str, obj:object) -> None:
    try:
        logging.info("Entered the save_object method of MainuUtils class")
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path, "wb") as file_obj:
            pickle.dump(obj,file_obj)
        logging.info("Exited the save_object method of MainuUtils class")
    except Exception as e:
        raise EcommerceException(e, sys)
    
def load_object(file_path: str, ) -> object:
    try:
        if not os.path.exists(file_path):
            raise Exception(f"The file: {file_path} is not exists")
        with open(file_path, "rb") as file_obj:
            print(file_obj)
            return pickle.load(file_obj)
    except Exception as e:
        raise EcommerceException(e, sys) 
    

def load_numpy_array_data(file_path: str) -> np.array:
    """
    load numpy array data from file
    file_path: str loaction of file to load
    return: np.array data loaded
    """
    
    try:
        with open(file_path, "rb") as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise EcommerceException(e, sys)
    