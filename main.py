from Ecommerce.components.data_ingestion import DataIngestion
from Ecommerce.components.data_validation import DataValidation
from Ecommerce.components.data_transformation import DataTransformation
from Ecommerce.entity.config_entity import DataValidationConfig
from Ecommerce.entity.config_entity import DataIngestionConfig,DataTransformataionConfig
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
        
        datatranformationconfig = DataTransformataionConfig(trainingpipelineconfig)
        data_tranformation  = DataTransformation(datavalidationartifact,datatranformationconfig)
        data_tranformation_artifact = data_tranformation.initiate_data_transformation()
        
        print(data_tranformation_artifact)
        
        print(datavalidationartifact)
    except Exception as e:
        raise EcommerceException