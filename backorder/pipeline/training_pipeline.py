from backorder.entity.config_entity import TrainingPipelineConfig, DataIngestionConfig
from backorder.entity.artifact_entity import DataIngestionArtifact
from backorder.exception import BackorderException
from backorder.logger import logging
import os, sys
from backorder.components.data_ingestion import DataIngestion

class TrainingPipeline:

    def __init__(self, training_pipeline_config:TrainingPipelineConfig):
        try:
            self.training_pipeline_config=training_pipeline_config
        except Exception as e:
            raise BackorderException(e, sys)

    def start_data_ingestion(self)->DataIngestionArtifact:
        try:
            data_ingestion_config = DataIngestionConfig(
                training_pipeline_config=self.training_pipeline_config)

            data_ingestion = DataIngestion(data_ingestion_config)

            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            return data_ingestion_artifact

        except Exception as e:
            raise BackorderException(e, sys)

    def start(self,):
        try:
            data_ingestion_artifact = self.start_data_ingestion()
        except Exception as e:
            raise BackorderException(e, sys)