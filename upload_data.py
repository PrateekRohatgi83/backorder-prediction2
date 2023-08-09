from backorder.utils import dump_csv_file_to_mongodb_collection
from backorder.exception import BackorderException
from backorder.logger import logging
import sys
import os

def storing_record_in_mongo():
    try:
        file_path = '/config/workspace/backorder.csv'
        database_name = 'backorder'
        collection_name = 'back_order'
        dump_csv_file_to_mongodb_collection(file_path, database_name, collection_name)
    except Exception as e:
        raise e

if __name__ == '__main__':
    storing_record_in_mongo()