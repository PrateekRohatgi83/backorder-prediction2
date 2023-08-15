from backorder.ml.model_resolver import ModelResolver
from backorder.ml.metric.classification_metric import get_classification_score
from backorder.entity.config_entity import ModelEvaluationConfig, DataTransformationConfig
from backorder.entity.artifact_entity import DataIngestionArtifact, DataTransformationArtifact, DataValidationArtifact, ModelEvaluationArtifact, ModelTrainerArtifact
from backorder.exception import BackorderException
from backorder.logger import logging
from backorder.config import TARGET_COLUMN, DROP_COLUMN
from backorder.utils import read_yaml_file, load_object
from backorder.ml.estimator import TargetValueMapping
from sklearn.metrics import f1_score
import pandas as pd
import os, sys

class ModelEvaluation:
    def __init__(self, model_evaluation_config: ModelEvaluationConfig, 
        model_evaluation_artifact: ModelEvaluationArtifact,
        data_transformation_config: DataTransformationConfig, 
        data_ingestion_artifact: DataIngestionArtifact, 
        data_transformation_artifact: DataTransformationArtifact,
        model_trainer_artifact: ModelTrainerArtifact,
        data_validation_artifact: DataValidationArtifact
        ):
        try:
            logging.info(f"{'>>'*20}  Model Evaluation {'<<'*20}")
            self.data_transformation_config = data_transformation_config
            self.model_evaluation_config = model_evaluation_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_transformation_artifact = data_transformation_artifact
            self.data_validation_artifact = data_validation_artifact
            self.model_trainer_artifact = model_trainer_artifact
            self.model_resolver = ModelResolver()
        except Exception as e:
            raise BackorderException(e, sys)

    def initiate_model_evaluation(self, data_transformation_config: DataTransformationConfig)->ModelEvaluationArtifact:
        try:
        #     # schema_info = read_yaml_file(file_path=self.data_transformation_config.schema_file_path)
        #     # target_column = schema_info["target_column"]

        #     logging.info("if saved model folder has model then we will compare which model is best trained or the model from sqaved model folder")
        #     latest_dir_path = self.model_resolver.get_latest_dir_path()
        #     if latest_dir_path == None:
        #         model_evaluation_artifact = ModelEvaluationArtifact(is_model_accepted=True, improved_accuracy=None)
        #         logging.info(f"Model evaluation artifact: {model_evaluation_artifact}")
        #         # return model_evaluation_artifact

        #     logging.info("Finding location of transformer, model and target encoder")
        #     model_path = self.model_resolver.get_latest_model_path()
        #     transformer_path = self.model_resolver.get_latest_transformer_path()
        #     target_encoder_path = self.model_resolver.get_latest_target_encoder_path()

        #     logging.info("Previous trained objects of transformer, model and target encoder")
        #     transformer = load_object(file_path=transformer_path)
        #     model = load_object(file_path=model_path)
        #     target_encoder = load_object(file_path=target_encoder_path)

        #     logging.info("Currently trained model objects")
        #     current_transformer = load_object(file_path=self.data_transformation_artifact.transform_object_path)
        #     current_model = load_object(file_path=self.model_trainer_artifact.model_path)
        #     current_target_encoder = load_object(file_path=self.data_transformation_artifact.target_encoder_path)

        #     test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)
            
        #     x = test_df.drop(TARGET_COLUMN, axis=1)
        #     x = x.drop(DROP_COLUMN, axis=1)
        #     x = x.replace({'Yes':1, 'No':0})
        #     y = test_df[TARGET_COLUMN]

        #     # trained_model = load_object(
        #     #     file_path=self.model_trainer_artifact.model_path
        #     # )

        #     y_true =target_encoder.transform(y)
        #     # y.replace(TargetValueMapping().to_dict(), inplace=True)
            
        #     # target_df = test_df[TARGET_COLUMN]
        #     # y_true = target_encoder.transform(target_df)

        #     logging.info("Accuracy using previous trained models")

        #     # input_feature_name = list(transformer.feature_names_in_)

        #     # input_arr = transformer.transform(test_df[input_feature_name])
        #     y_pred = model.predict(x)

        #     print(f"Prediction using previous model: {target_encoder.inverse_transform(y_pred[:5])}")
        #     previous_model_score = f1_score(y_true=y_true, y_pred=y_pred)
        #     logging.info(f"Accuracy using previous trained model: {previous_model_score}")

        #     logging.info("Accuracy using current trained model")
        #     # input_feature_name = list(current_transformer.feature_names_in_)
        #     # input_arr = current_transformer.transform(test_df[input_feature_name])
            
        #     # y_pred = current_model.predict(input_arr)
        #     # y_true = current_target_encoder.transform(target_df)

        #     y_predict = current_model.predict(x)
        #     y_truth = current_target_encoder.transform(y)

        #     print(f"Prediction using trained model: {current_target_encoder.inverse_transform(y_pred[:5])}")
        #     current_model_score = f1_score(y_true=y_truth, y_pred=y_predict)
        #     logging.info(f"Accuracy using current trained model: {current_model_score}")
        #     if current_model_score <= previous_model_score:
        #         logging.info(f"Current trained model is not better than previous trained model")
        #         raise Exception("Current trained model is not better than previous trained model")

        #     model_evaluation_artifact = ModelEvaluationArtifact(is_model_accepted=True, improved_accuracy=current_model_score-previous_model_score)
        #     logging.info(f"Model evaluation artifact: {model_evaluation_artifact}")
        #     return model_evaluation_artifact
            train_file_path = self.data_validation_artifact.train_file_path
            test_file_path = self.data_validation_artifact.test_file_path

            train_df = pd.read_csv(train_file_path)
            test_df = pd.read_csv(test_file_path)

            df = pd.concat([train_df,test_df])
            y_true = df[TARGET_COLUMN]
            y_true.replace(TargetValueMapping().to_dict(),inplace=True)
            df.drop(TARGET_COLUMN,axis=1,inplace=True)

            train_model_file_path = self.model_trainer_artifact.model_path
            model_resolver = ModelResolver()
            is_model_accepted=True

            if not model_resolver.is_model_exists():
                model_evaluation_artifact = ModelEvaluationArtifact(
                    is_model_accepted = is_model_accepted, 
                    improved_accuracy = None, 
                    best_model_path = None, 
                    trained_model_path = train_model_file_path
            )

            logging.info(f"Model evaluation artifact: {model_evaluation_artifact}")
            # return model_evaluation_artifact

            latest_model_path = model_resolver.get_best_model_path()
            latest_model = load_object(file_path=latest_model_path)
            train_model = load_object(file_path=train_model_file_path)
            
            y_trained_pred = train_model.predict(df)
            y_latest_pred  = latest_model.predict(df)

            trained_metric = get_classification_score(y_true, y_trained_pred)
            latest_metric = get_classification_score(y_true, y_latest_pred)

            improved_accuracy = trained_metric.f1_score-latest_metric.f1_score
            if self.model_evaluation_config.change_threshold < improved_accuracy:
                is_model_accepted=True
            else:
                is_model_accepted=False

            model_evaluation_artifact = ModelEvaluationArtifact(
                    is_model_accepted=is_model_accepted, 
                    improved_accuracy=improved_accuracy, 
                    best_model_path=latest_model_path, 
                    trained_model_path=train_model_file_path, 
            )

            model_evaluation_report = model_evaluation_artifact.__dict__

            write_yaml_file(self.model_evaluation_config.report_file_path, model_evaluation_report)
            logging.info(f"Model evaluation artifact: {model_evaluation_artifact}")
            return model_evaluation_artifact

        except Exception as e:
            raise BackorderException(e, sys)