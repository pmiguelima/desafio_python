from pymongo import MongoClient

client = MongoClient("mongodb://root:MongoDB2019!@mongo:27017")
database = client['test']
collection = database['default']
insights_collection = database['insights']


def insert_dataframe_to_db(df):
    collection.insert_many(df.to_dict('records'))
