from backorder.ml.model_resolver import ModelResolver
from backorder.entity.config_entity import ModelEvaluationConfig, DataTransformationConfig
from backorder.entity.artifact_entity import DataIngestionArtifact, DataTransformationArtifact, ModelEvaluationArtifact, ModelTrainerArtifact
from backorder.exception import BackorderException
from backorder.logger import logging
from backorder.config import TARGET_COLUMN
from backorder.utils import read_yaml_file, load_object
from sklearn.metrics import f1_score
import pandas as pd
import os, sys

class ModelEvaluation:
    def __init__(self, model_evaluation_config: ModelEvaluationConfig, 
        model_evaluation_artifact: ModelEvaluationArtifact,
        data_transformation_config: DataTransformationConfig, 
        data_ingestion_artifact: DataIngestionArtifact, 
        data_transformation_artifact: DataTransformationArtifact,
        model_trainer_artifact: ModelTrainerArtifact
        ):
        try:
            logging.info(f"{'>>'*20}  Model Evaluation {'<<'*20}")
            self.data_transformation_config = data_transformation_config
            self.model_evaluation_config = model_evaluation_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_transformation_artifact = data_transformation_artifact
            self.model_trainer_artifact = model_trainer_artifact
            self.model_resolver = ModelResolver()
        except Exception as e:
            raise BackorderException(e, sys)

    def initiate_model_evaluation(self, data_transformation_config: DataTransformationConfig)->ModelEvaluationArtifact:
        try:
            # schema_info = read_yaml_file(file_path=self.data_transformation_config.schema_file_path)
            # target_column = schema_info["target_column"]

            logging.info("if saved model folder has model then we will compare which model is best trained or the model from sqaved model folder")
            latest_dir_path = self.model_resolver.get_latest_dir_path()
            if latest_dir_path == None:
                model_evaluation_artifact = ModelEvaluationArtifact(is_model_accepted=True, improved_accuracy=None)
                logging.info(f"Model evaluation artifact: {model_evaluation_artifact}")
                # return model_evaluation_artifact

            logging.info("Finding location of transformer, model and target encoder")
            transformer_path = self.model_resolver.get_latest_transformer_path()
            model_path = self.model_resolver.get_latest_model_path()
            target_encoder_path = self.model_resolver.get_latest_target_encoder_path()

            logging.info("Previous trained objects of transformer, model and target encoder")
            transformer = load_object(file_path=transformer_path)
            model = load_object(file_path=model_path)
            target_encoder = load_object(file_path=target_encoder_path)

            logging.info("Currently trained model objects")
            current_transformer = load_object(file_path=self.data_transformation_artifact.transform_object_path)
            current_model = load_object(file_path=self.model_trainer_artifact.model_path)
            current_target_encoder = load_object(file_path=self.data_transformation_artifact.target_encoder_path)

            test_df = pd.read_csv(self.data_validation_artifact.test_file_path)
            target_df = test_df[target_column]
            y_true = target_encoder.transform(target_df)

            logging.info("Accuracy using previous trained models")
            input_feature_name = list(transformer.feature_names_in_)
            input_arr = transformer.transform(test_df[input_feature_name])
            y_pred = model.predict(input_arr)
            print(f"Prediction using previous model: {target_encoder.inverse_transform(y_pred[:5])}")
            previous_model_score = f1_score(y_true=y_true, y_pred=y_pred)
            logging.info(f"Accuracy using previous trained model: {previous_model_score}")

            logging.info("Accuracy using current trained model")
            input_feature_name = list(current_transformer.feature_names_in_)
            input_arr = current_transformer.transform(test_df[input_feature_name])
            y_pred = current_model.predict(input_arr)
            y_true = current_target_encoder.transform(target_df)
            print(f"Prediction using trained model: {current_target_encoder.inverse_transform(y_pred[:5])}")
            current_model_score = f1_score(y_true=y_true, y_pred=y_pred)
            logging.info(f"Accuracy using current trained model: {current_model_score}")
            if current_model_score <= previous_model_score:
                logging.info(f"Current trained model is not better than previous trained model, so we will accept the model")
                raise Exception("Current trained model is not better than previous trained model")

            model_evaluation_artifact = ModelEvaluationArtifact(is_model_accepted=True, improved_accuracy=current_model_score-previous_model_score)
            logging.info(f"Model evaluation artifact: {model_evaluation_artifact}")
            return model_evaluation_artifact
        except Exception as e:
            raise BackorderException(e, sys)