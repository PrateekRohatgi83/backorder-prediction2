from backorder.entity.config_entity import TrainingPipelineConfig, DataIngestionConfig, DataValidationConfig, DataTransformationConfig
from backorder.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact, DataTransformationArtifact
from backorder.exception import BackorderException
from backorder.logger import logging
import os, sys
from backorder.components.data_ingestion import DataIngestion
from backorder.components.data_validation import DataValidation
from backorder.components.data_transformation import DataTransformation

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

    def start_data_validation(self, data_ingestion_artifact:DataIngestionArtifact)->DataValidationArtifact:
        try:
            data_validation_config = DataValidationConfig(
                training_pipeline_config=self.training_pipeline_config)
            data_validation = DataValidation(data_validation_config=data_validation_config, 
            data_ingestion_artifact=data_ingestion_artifact)

            return data_validation.initiate_date_validation()

        except Exception as e:
            raise BackorderException(e, sys)

    def start_data_transformation(self, data_validation_artifact:DataValidationArtifact)->DataValidationArtifact:
        try:
            data_transformation_config = DataTransformationConfig(
                training_pipeline_config=self.training_pipeline_config)
            data_transformation = DataTransformation(data_transformation_config=data_transformation_config, 
            data_validation_artifact=data_validation_artifact)

            return data_transformation.initiate_data_transformation()

        except Exception as e:
            raise BackorderException(e, sys)
        

    def start(self,):
        try:
            data_ingestion_artifact = self.start_data_ingestion()

            data_validation_artifact = self.start_data_validation(
                data_ingestion_artifact=data_ingestion_artifact)
                
            data_transformation_artifact = self.start_data_transformation(
                data_validation_artifact=data_validation_artifact
            )
        except Exception as e:
            raise BackorderException(e, sys)