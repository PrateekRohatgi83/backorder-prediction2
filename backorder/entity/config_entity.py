from datetime import datetime
import os, sys  
from backorder.exception import BackorderException
TRAIN_FILE_NAME = "train.csv"
TEST_FILE_NAME = "test.csv"
TRANSFORMER_OBJECT_FILE_NAME = "transformer.pkl"
TARGET_ENCODER_OBJECT_FILE_NAME = "target_encoder.pkl"
MODEL_FILE_NAME = "model.pkl"

class TrainingPipelineConfig:
    def __init__(self): 
        timestamp = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
        self.artifact_dir = os.path.join("artifact", timestamp)

class DataIngestionConfig:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        try:
            data_ingestion_dir = os.path.join(training_pipeline_config.artifact_dir, "data_ingestion")
            self.dataset_dir = os.path.join(data_ingestion_dir, "dataset")
            self.train_file_path = os.path.join(self.dataset_dir, TRAIN_FILE_NAME)
            self.test_file_path = os.path.join(self.dataset_dir, TEST_FILE_NAME)
            self.database_name = "backorder"
            self.collection_name = "back_order"
            self.test_size = 0.2
        except Exception as e:
            raise BackorderException(e, sys)

    def to_dict(self,)->dict:
        try:
            return self.__dict__
        except Exception  as e:
            raise BackorderException(e, sys)

class DataValidationConfig:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        try:
            data_validation_dir = os.path.join(training_pipeline_config.artifact_dir, "data_validation")
            self.valid_dir = os.path.join(data_validation_dir, "valid")
            self.invalid_dir = os.path.join(data_validation_dir, "invalid")
            self.valid_train_file_path = os.path.join(self.valid_dir, TRAIN_FILE_NAME)
            self.invalid_train_file_path = os.path.join(self.invalid_dir, TRAIN_FILE_NAME)
            self.valid_test_file_path = os.path.join(self.valid_dir, TEST_FILE_NAME)
            self.invalid_test_file_path = os.path.join(self.invalid_dir, TEST_FILE_NAME)
            self.report_file_name = os.path.join(data_validation_dir, "report", "report.yaml") 
            self.schema_file_path = os.path.join("schema.yaml")
            self.missing_threshold = 5
        except Exception as e:
            raise BackorderException(e, sys)

class DataTransformationConfig:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        try:
            data_transformation_dir = os.path.join(training_pipeline_config.artifact_dir, "data_transformation")
            self.transform_obj_dir = os.path.join(data_transformation_dir, "transformer")      
            self.transform_object_path = os.path.join(self.transform_obj_dir,TRANSFORMER_OBJECT_FILE_NAME)
            self.transform_data = os.path.join(data_transformation_dir, "transform_data")
            self.transform_train_path = os.path.join(self.transform_data,TRAIN_FILE_NAME.replace("csv", "npz"))
            self.transform_test_path = os.path.join(self.transform_data,TEST_FILE_NAME.replace("csv", "npz"))
            self.target_encoder_path = os.path.join(data_transformation_dir, "target_encoder", TARGET_ENCODER_OBJECT_FILE_NAME)
            self.schema_file_path = os.path.join("schema.yaml")
        except Exception as e:
            raise BackorderException(e, sys)

class ModelTrainerConfig:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        try:
            model_trainer_dir = os.path.join(training_pipeline_config.artifact_dir, "model_trainer")
            self.model_path = os.path.join(model_trainer_dir, "model", MODEL_FILE_NAME)
            self.expected_score = 0.8
            self.overfitting_threshold = 0.1

        except Exception as e:
            raise BackorderException(e, sys)

# class ModelEvaluationConfig:
#     def __init__(self, training_pipeline_config:TrainingPipelineConfig):
#         try:
#             self.change_threshold = 0.01
#         except Exception as e:
#             raise BackorderException(e, sys)

class ModelPusherConfig:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        self.model_pusher_dir = os.path.join(training_pipeline_config.artifact_dir, "model_pusher")
        self.saved_model_dir = os.path.join("saved_models")
        self.pusher_model_dir = os.path.join(self.model_pusher_dir,"saved_models")
        self.pusher_model_path = os.path.join(self.pusher_model_dir, MODEL_FILE_NAME)
        self.pusher_transformer_path = os.path.join(self.pusher_model_dir, TRANSFORMER_OBJECT_FILE_NAME)
        self.pusher_target_encoder_path = os.path.join(self.pusher_model_dir, TARGET_ENCODER_OBJECT_FILE_NAME)

class ModelEvaluationConfig:
    def __init__(self, training_pipeline_config:TrainingPipelineConfig):
        try:
            self.model_evaluation_dir: str = os.path.join(
            training_pipeline_config.artifact_dir, "model_evaluation")
            self.change_threshold = 0.01
            self.report_file_path = os.path.join(self.model_evaluation_dir,"report.yaml")
        except Exception as e:
            raise BackorderException(e, sys)