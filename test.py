from backorder.utils import dump_csv_file_to_mongodb_collection
from backorder.exception import BackorderException
from backorder.logger import logging
import sys
import os

def storing_record_in_mongo():
    try:
        file_path = '/config/workspace/back_order.csv'
        database_name = 'backorder'
        collection_name = 'back_order'
        dump_csv_file_to_mongodb_collection(file_path, database_name, collection_name)
    except Exception as e:
        raise e

def test_exception_and_logger():
    try:
        x = 1/0
    except Exception as e:
        raise BackorderException(e, sys)

if __name__ == '__main__':
    try:
        test_exception_and_logger()
    except Exception as e:
        logging.info(f"error: {e}")
        print(e)