from Ecommerce.components.data_ingestion import DataIngestion
from Ecommerce.components.data_validation import DataValidation
from Ecommerce.components.data_transformation import DataTransformation
from Ecommerce.entity.config_entity import DataValidationConfig
from Ecommerce.entity.config_entity import DataIngestionConfig,DataTransformataionConfig
from Ecommerce.entity.config_entity import TrainingPipelineConfig
from Ecommerce.exception.exception import EcommerceException
from Ecommerce.entity.config_entity import ModelTrainerConfig
from Ecommerce.components.model_trainer import ModelTrainer
from Ecommerce.entity.artifact_entity import ModelTrainerArtifact



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
        
        model_trainer_config = ModelTrainerConfig(trainingpipelineconfig)
        model_trainer = ModelTrainer(data_tranformation_artifact,model_trainer_config)
        
        model_trainer_artifact  = model_trainer.initiate_model_trainer()
    except Exception as e:
        raise EcommerceException