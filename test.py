import certifi
import json
import math
import argparse
import pandas as pd
import subprocess
import pymongo
import datetime

from bson import ObjectId
from DBUtils import DBUtils
from Document import Document

uri = 'mongodb+srv://celegaspino:legO2814@cluster.gzxgs.mongodb.net/?retryWrites=true&w=majority&appName=cluster'

db_name = 'rok'
collection_name = 'scan'
backup_dir = '/Users/miri/Desktop/dong/rok/scan'


db = DBUtils(uri, db_name)

def load_file(file_name):
   try:
      dataframe = pd.read_excel(file_name, header=0)

      # Check for any NaN, Null, or Empty Cells
      mask = dataframe.isna() | (dataframe == '')
      if mask.any().any():
         bad_data = mask[mask].stack().index.tolist()
         print('Location:',bad_data)
         raise Exception("Program failed. Bad or empty data contained in file")

      # Check 'ID' column for any duplicates
      duplicates = dataframe.loc[dataframe.duplicated(subset=['ID'], keep=False)]
      if not duplicates.empty:
         print('Duplicate Rows:\n', duplicates)
         raise Exception("Program failed. Duplicate IDs found.")

      return dataframe
   except Exception as e:
      print(f'Error: load_file() >> {e}')

def process():
   try:
      df = load_file('new_scan.xlsx')
      #test_obj = db.fetch_one(collection_name, '54605299')
      
      if df is not None:
         for index, row in df.iterrows():
            print(index)
            _filter = str(row['ID'])
            document = db.fetch_one(collection_name, _filter)

            if document is None:
               print(_filter)
               continue

            doc = Document.from_dict(document)
            x = int(row['Kill Points'].replace(',','')) - doc.kp
            df.at[index, 'KP Gained'] = f"{x:,}"

         df.to_excel('updated_new_scan.xlsx', index=False)


   except Exception as e:
      print(e)

def backup():
   print('heehee')

   collections = db.list_collection()
   print(collections)

   now = datetime.datetime.now()
   dtf = now.strftime('%Y%m%d_%H-%M-%S')
   df = now.strftime('%Y_%m_%d')
   
   for collection in collections:
      file = f"{backup_dir}/backup/{df}/{dtf}_{collection}_BAK.json"
      command = [
         'mongoexport',
         '--uri', uri,
         '--db', db_name,
         '--collection', collection,
         '--out', file,
         '--jsonArray'
      ]

      try:
         result = subprocess.run(command, check=True, text=True, capture_output=True)
         print(f"Backup of collection '{collection}' saved to {file}")
         print(f"stdout: {result.stdout}")  # Print any standard output (if needed)
      except subprocess.CalledProcessError as e:
         print(f"Error exporting collection '{collection}': {e}")
         print(f"stderr: {e.stderr}")  # Print any standard error output
         break
   
   print("Database backup completed successfully.")


def update():
   try:
      df = load_file('test.xlsx')
      
      if df is not None:
         collection_list = db.fetch_all(collection_name)

         for index, row in df.iterrows():
            filter = str(row['ID'])
            update = {
               'name': row['Name'],
               'power': int(row['Power'].replace(',','')),
               'kp': int(row['Kill Points'].replace(',','')),
               'deaths': int(row['Deaths'].replace(',','')),
               't4': int(row['T4 Kills'].replace(',','')),
               't5': int(row['T5 Kills'].replace(',',''))
            }

            #result = db.update(collection_name, filter, update)

   except Exception as e:
      print(f'Error: update() >> {e}')
      return
def ping():
   db.client.admin.command('ping')
   print('Ping successful')

if __name__ == "__main__":
   parser = argparse.ArgumentParser(description="ROK Scan Automation")
   parser.add_argument('-a','--action',
      choices=[
         'process',
         'update',
         'backup',
         'ping'], 
      default='process', 
      help="Available actions for program to preform"
   )
   parser.add_argument('-f','--file', help="The file to process")

   args = parser.parse_args()
   if args.action == 'process':
      process()
   elif args.action == 'backup':
      backup()
   elif args.action == 'update':
      update()
   elif args.action == 'ping':
      ping()
   else:
      print('noice')