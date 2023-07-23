from backorder.exception import BackorderException
from backorder.logger import logging
from backorder.entity.artifact_entity import DataIngestionArtifact
from backorder.entity.config_entity import  DataIngestionConfig
from backorder.utils import export_collection_as_dataframe
from sklearn.model_selection import train_test_split
import sys
import os
import numpy as np

class DataIngestion:

    def __init__(self, data_ingestion_config: DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise BackorderException(e, sys)

    def initiate_data_ingestion(self)->DataIngestionArtifact:
        try:
            logging.info("Exporting collection as dataframe")
            df = export_collection_as_dataframe(
                database_name = self.data_ingestion_config.database_name, 
                collection_name = self.data_ingestion_config.collection_name)

            logging.info("replacing null with nan")
            df.replace({"null": np.nan}, inplace=True)

            logging.info("splitting data into train and test set")
            train_df, test_df = train_test_split(df, test_size=self.data_ingestion_config.test_size)

            logging.info("creating dataset directory")
            os.makedirs(self.data_ingestion_config.dataset_dir, exist_ok=True)
            
            logging.info("saving train and test file")
            train_df.to_csv(self.data_ingestion_config.train_file_path, header=True)
            test_df.to_csv(self.data_ingestion_config.test_file_path, header=True)

            logging.info("Preparing data ingestion artifact")
            data_ingestion_artifact = DataIngestionArtifact(train_file_path=self.data_ingestion_config.train_file_path, 
            test_file_path = self.data_ingestion_config.test_file_path)

            logging.info(f"Data ingestion artifact: {data_ingestion_artifact}")
            return data_ingestion_artifact


        except Exception as e:
            raise BackorderException(e, sys)