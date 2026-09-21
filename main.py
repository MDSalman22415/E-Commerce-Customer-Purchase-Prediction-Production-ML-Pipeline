from Ecommerce.components.data_ingestion import DataIngestion
from Ecommerce.components.data_validation import DataValidation
from Ecommerce.entity.config_entity import DataValidationConfig
from Ecommerce.entity.config_entity import DataIngestionConfig
from Ecommerce.entity.config_entity import TrainingPipelineConfig
from Ecommerce.exception.exception import EcommerceException


if __name__=="__main__":
    try:
        trainingpipelineconfig = TrainingPipelineConfig()
        dataingestionconfig = DataIngestionConfig(trainingpipelineconfig)
        data_ingestion = DataIngestion(dataingestionconfig)
        
        dataingestionartifact = data_ingestion.initiate_data_ingestion()
        
        print(dataingestionartifact)
        
        datavalidationcofig = DataValidationConfig(trainingpipelineconfig)
        data_validation = DataValidation(dataingestionartifact,datavalidationcofig)
        
        datavalidationartifact = data_validation.initaite_data_validation()
        
        print(datavalidationartifact)
    except Exception as e:
        raise EcommerceException