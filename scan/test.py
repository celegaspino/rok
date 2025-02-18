import certifi
import json
import math
import argparse
import pandas as pd

from bson import ObjectId
from DBUtils import DBUtils
from Document import Document

uri = 'mongodb+srv://<username>:<password>@<cluster>.gzxgs.mongodb.net/?retryWrites=true&w=majority&appName=<cluser>'

db_name = 'rok'
collection_name = 'scan'

out_file = 'dump.json'

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
      db.client.admin.command('ping')
      print('Ping successful')

   except Exception as e:
      print(e)

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

            result = db.update(collection_name, filter, update)

   except Exception as e:
      print(f'Error: update() >> {e}')
      return

if __name__ == "__main__":
   parser = argparse.ArgumentParser(description="ROK Scan Automation")
   parser.add_argument('-a','--action',
      choices=[
         'process',
         'update'], 
      default='process', 
      help="Available actions for program to preform"
   )
   parser.add_argument('-f','--file', help="The file to process")

   args = parser.parse_args()
   if args.action == 'process':
      process()
   elif args.action == 'update':
      update()
   else:
      print('noice')