import sys
import pandas as pd
import pymongo
import certifi
from dotenv import load_dotenv
from Ecommerce.logging.logger import logging
from Ecommerce.exception.exception import EcommerceException
import os

load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")

ca = certifi.where()

class EcommerceDataExtract:
    
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise EcommerceException(e, sys)
    
    def csv_to_json_converter(self, file_path):
        try:
            ## Read CSv
            data = pd.read_csv(file_path)
            
            ### Reset index
            data.reset_index(drop=True, inplace=True)
            
            ## Convert Dataframe into list of dictionaries
            records = data.to_dict(orient="records")
            
            return records
        except Exception as e:
            raise EcommerceException(e, sys)
        
    def insert_data(self,records, database, collection):
        try:
            self.records = records
            
            ## Connect to MongoDB
            self.mongo_client = pymongo.MongoClient(
                MONGO_DB_URL,
            )
            
            ## Select Database
            self.database =self.mongo_client[database]
            
            ## Select collection
            self.collection = self.database[collection]
            
            ## Insert records
            self.collection.insert_many(self.records)
            
            return len(self.records)
        except Exception as e:
            raise EcommerceException(e, sys)
        

if __name__=="__main__":
    
    FILE_PATH = "E-commerce_data/Cleaned_data.csv"
    DATABASE  = "Ecommerce"
    COLLECTION = "Ecommercedata"
    
    ecommerce_obj = EcommerceDataExtract()
    
    records = ecommerce_obj.csv_to_json_converter(FILE_PATH)
    
    print(f"Total records:{len(records)}")
    
    # Insert inot mongodb
    no_of_records = ecommerce_obj.insert_data(
        records,
        DATABASE,
        COLLECTION
    )
    
    print(f"Inserted records :{no_of_records}")