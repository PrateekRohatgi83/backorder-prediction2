from dataclasses import dataclass
import json
import pandas as pd
import pymongo
import os, sys

MONGO_DB_URL_ENV_KEY = "MONGO_DB_URL"

@dataclass
class EnvironmentVariable:
    mongo_db_url: str = os.getenv(MONGO_DB_URL_ENV_KEY)

env_var = EnvironmentVariable()
mongo_client = pymongo.MongoClient(env_var.mongo_db_url)
TARGET_COLUMN = "went_on_backorder"
DROP_COLUMN = 'lead_time'