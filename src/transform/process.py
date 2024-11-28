from datetime import datetime
from src.load.database import insert_dataframe_to_db, collection

import pandas as pd
import traceback
from concurrent.futures import ThreadPoolExecutor


def transform_data(df):
    df['createdAt'] = datetime.now().isoformat(timespec='milliseconds')
    
    for column in df.columns:
        if df[column].dtype.kind in 'biufc':
            df[column] = df[column].fillna(value=0)
        elif df[column].dtype == 'object':
            df[column] = df[column].fillna(value=None)
    return df

def process_file(file, chunks_size):
    try:
        with pd.read_csv(file, chunksize=chunks_size) as reader:
            for chunk in reader:
                processed_chunk = chunk
                insert_dataframe_to_db(processed_chunk)
    except Exception as e:
        print(f"Erro ao processar o arquivo {file}: {e}\nError: {str(traceback.format_exc())}")


def parallel_file_execution(file_list, chunk_size=1000, max_workers=4):
   
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [
            executor.submit(
                process_file,
                file,
                chunk_size
            )
            for file in file_list
        ]

        for future in futures:
            future.result()

def get_calculete_insights():
    data = pd.DataFrame(list(collection.find()))
    
    if "_id" in data.columns:
        data.drop(columns=["_id"], inplace=True)

    delay_columns = [
        "CARRIER_DELAY",
        "WEATHER_DELAY",
        "NAS_DELAY",
        "SECURITY_DELAY",
        "LATE_AIRCRAFT_DELAY"
    ]

    return data.groupby([
        "OP_CARRIER",
        "OP_CARRIER_FL_NUM",
        "ORIGIN"
    ]).agg(
        avg_delay=pd.NamedAgg(column=delay_columns, aggfunc=lambda x: x.fillna(0).sum(axis=1).mean()),
        total_air_time=pd.NamedAgg(column="AIR_TIME", aggfunc="sum"),
        cancel_chance=pd.NamedAgg(column="CANCELLED", aggfunc="mean"),
    ).reset_index()