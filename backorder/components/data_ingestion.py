from backorder.exception import BackorderException
from backorder.logger import logging
from backorder.entity.artifact_entity import DataIngestionArtifact
from backorder.entity.config_entity import DataIngestionConfig
from backorder.utils import export_collection_as_dataframe
from sklearn.model_selection import train_test_split
import os, sys
from dataclasses import dataclass
import numpy as np
import pandas as pd

class DataIngestion:
    def __init__(self, data_ingestion_config:DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise BackorderException(e, sys)

    def initiate_data_ingestion(self)->DataIngestionArtifact:
        logging.info("initiating data ingestion")
        try:
            logging.info("Exporting collection as dataframe")
            df = export_collection_as_dataframe(
                database_name = self.data_ingestion_config.database_name,
                collection_name = self.data_ingestion_config.collection_name)
            # logging.info("read data as data frame")
            # df = pd.read_csv("notebook/data/backorder_dataset.csv", low_memory=False)
            # os.makedirs(os.path.dirname(self.data_ingestion_config.raw_data_path), exist_ok=True)
            # df.to_csv(self.data_ingestion_config.raw_data_path, header=True, index=False)
            
            logging.info("Replacing null with NAN")
            df.replace({"null":np.NAN},inplace=True)
            
            logging.info("removing sku column")
            df = df.drop(columns=['sku'], axis=1)

            # logging.info("removing lead_time column")
            # df = df.drop(columns=['lead_time'], axis=1)

            logging.info("removing duplicates")
            df = df.drop_duplicates(ignore_index=True)

            logging.info("splitting data into train and test and saving it")
            # train_set, test_set = train_test_split(df, test_size=0.25, random_state=42)
            train_df, test_df = train_test_split(df, test_size=self.data_ingestion_config.test_size)
            os.makedirs(self.data_ingestion_config.dataset_dir, exist_ok=True)

            logging.info("Saving train and test file.")
            train_df.to_csv(self.data_ingestion_config.train_file_path, index=False, header=True)
            test_df.to_csv(self.data_ingestion_config.test_file_path, index=False, header=True)
            
            logging.info("Preparing data ingestion artifact")
            data_ingestion_artifact = DataIngestionArtifact(train_file_path=self.data_ingestion_config.train_file_path, 
            test_file_path=self.data_ingestion_config.test_file_path)

            logging.info(f"Data ingestion artifact: {data_ingestion_artifact}")
            return data_ingestion_artifact

            # logging.info("data ingestion completed")
            # return artifacts_entity.DataIngestionArtifacts(
            #     self.data_ingestion_config.train_data_path,
            #     self.data_ingestion_config.test_data_path
            # )
            
        except Exception as e:
            raise BackorderException(e, sys)