# db_writer.py
import pyodbc
from pymongo import MongoClient
from datetime import datetime
from logger import get_logger

logger = get_logger(__name__)

class DBWriter:

    def __init__(self, sql_config=None, mongo_uri=None):
        self.sql_config = sql_config
        self.mongo_uri = mongo_uri

    # ---------------- SQL SERVER ----------------
    def write_sql(self, sp_name, params):
        try:
            conn = pyodbc.connect(
                f"Driver={self.sql_config['driver']};"
                f"Server={self.sql_config['server']};"
                f"Database={self.sql_config['database']};"
            )
            conn.autocommit = True
            cursor = conn.cursor()
            cursor.execute(sp_name, params)
            result = cursor.fetchone()
            cursor.close()
            conn.close()
            return result

        except Exception as e:
            logger.error("SQL write failed", exc_info=True)
            raise e

    # ---------------- MONGODB ----------------
    def write_mongo(self, db_name, collection_name, document):
        try:
            client = MongoClient(self.mongo_uri)
            collection = client[db_name][collection_name]
            result = collection.insert_one(document)
            logger.info(f"Mongo inserted ID: {result.inserted_id}")
            return result.inserted_id
        except Exception:
            logger.error("Mongo insert failed", exc_info=True)
            return None