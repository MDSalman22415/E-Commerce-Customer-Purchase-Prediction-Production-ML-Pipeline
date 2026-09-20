from Ecommerce.components.data_ingestion import DataIngestion
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
    except Exception as e:
        raise EcommerceException