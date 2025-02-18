import certifi

from datetime import datetime

from bson import ObjectId
from Document import Document
from pymongo.mongo_client import MongoClient
from pymongo.errors import ServerSelectionTimeoutError, ConfigurationError, NetworkTimeout
from pymongo.server_api import ServerApi

class DBUtils:
	def __init__(self, uri, db_name):
		self.client = self.set_connection(uri)
		self.db = self.client[db_name]

	def __getitem__(self, collection):
		return self.db[collection]

	def set_connection(self, uri):
		try:
			mc = MongoClient(uri, server_api=ServerApi(version='1', strict=True, deprecation_errors=True), tlsCAFile=certifi.where())
			
			return mc
		except ServerSelectionTimeoutError as stte:
			print(f"Error DBUtils.set_connection()\nServerSelectionTimeoutError: MongoDB server selection timeout. {stte}")
		except NetworkTimeout as nt:
			print(f"Error DBUtils.set_connection()\nNetworkTimeout: MongoDB network connection timeout. {nt}")
		except ConfigurationError as cfg_err:
			print(f"Error DBUtils.set_connection()\nConfigurationError: There was an error in the configuration. {cfg_err}")
		except Exception as e:
			print(f"Error DBUtils.set_connection()\nAn unexpected error occurred: {e}")

	def close_connection(self):
		self.client.close()

	def fetch_all(self, collection_name):
		collection = self.db[collection_name]

		try:
			documents = collection.find()

			obj_list = [Document(
					doc.get('pid', 0),
					doc.get('name', 'Unknown'),
					doc.get('power', 0),
					doc.get('kp', 0),
					doc.get('deaths', 0),
					doc.get('t4', 0),
					doc.get('t5', 0)
				) for doc in documents
			]

			return obj_list
		except Exception as e:
			print(f'Error DBUtils.fetch_all():{e}')

	def update(self, collection_name, filter_pid, update_data):
		collection = self.db[collection_name]

		try:
			filter_insert = {'pid': filter_pid}
			update_insert = {'$set': update_data}

			result = collection.update_one(filter_insert, update_insert, upsert=True)
			if result.matched_count > 0:
				print(f'>> Updated existing entry \'{filter_pid}\'')
			else:
				print(f'++ Created new entry \'{filter_pid}\'')
		except Exception as e:
			print(f'Error DBUtils.update()\n{filter_pid}:{e}')
