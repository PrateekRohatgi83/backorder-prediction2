from backorder.entity.config_entity import DataValidationConfig
from backorder.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from backorder.logger import logging
from backorder.exception import BackorderException
import os, sys
import numpy as np
import pandas as pd

class DataValidation:

    def __init__(self, data_validation_config: DataValidationConfig, 
        data_ingestion_artifact: DataIngestionArtifact
        ):
        try:
            self.data_validation_config = data_validation_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self.validation_error = dict()

        except Exception as e:
            raise BackorderException(e, sys)

    def drop_missing_values_columns(self, df:pd.DataFrame, report_key_name:str)->Optional[pd.DataFrame]:
        try:
            threshold = self.data_validation_config.missing_threshold
            null_report = (df.isna().sum()*100)/df.shape[0]
            logging.info(f"selecting column name which contains null above to {threshold}")
            drop_column_names = null_report[null_report>threshold].index
            logging.info(f"Columns to drop: {list(drop_column_names)}")
            self.validation_error[report_key_name] = list(drop_column_names)
            df.drop(list(drop_column_names), axis=1, inplace=True)

            if len(df.columns) == 0:
                return None
            return df

        except Exception as e:
            raise BackorderException(e, sys)
        