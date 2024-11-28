#!/usr/bin/env python
import time, os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import numpy as np

from src.load.database import insights_collection, collection


async def main(file_list):
    pass


if __name__ == "__main__":
    start = time.time()
    print(f"Início: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start))}")
    
    # main(files)
    
    finish = time.time()
    print(f"Fim: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(finish))}")
    print(f"Tempo de execução: {finish - start:.6f} segundos")
    






data = pd.DataFrame(list(collection.find()))

# Remove o campo "_id" para evitar problemas
if "_id" in data.columns:
    data.drop(columns=["_id"], inplace=True)

# --- ETAPA 1: Calcula os Insights ---

# Campos de delay
delay_columns = [
    "CARRIER_DELAY",
    "WEATHER_DELAY",
    "NAS_DELAY",
    "SECURITY_DELAY",
    "LATE_AIRCRAFT_DELAY"
]

# Calcula a média de tempo de delay por linha aérea, número do voo e origem
insights = data.groupby(["OP_CARRIER", "OP_CARRIER_FL_NUM", "ORIGIN"]).agg(
    avg_delay=pd.NamedAgg(column=delay_columns, aggfunc=lambda x: x.fillna(0).sum(axis=1).mean()),
    total_air_time=pd.NamedAgg(column="AIR_TIME", aggfunc="sum"),
    cancel_chance=pd.NamedAgg(column="CANCELLED", aggfunc="mean"),
).reset_index()


# --- ETAPA 2: Cria o Modelo para Chance de Cancelamento ---

# Filtra os dados relevantes para o modelo
model_data = data.copy()
model_data.fillna(0, inplace=True)  # Substitui valores nulos por 0
X = model_data[[
    "DEP_DELAY",
    "ARR_DELAY",
    "AIR_TIME",
    "DISTANCE",
    "CARRIER_DELAY",
    "WEATHER_DELAY",
    "NAS_DELAY",
    "SECURITY_DELAY",
    "LATE_AIRCRAFT_DELAY"
]]
y = model_data["CANCELLED"]

# Divisão em treino e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Treinamento de um modelo simples (Random Forest)
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# Avaliação do modelo
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Acurácia do modelo: {accuracy:.2f}")

# Aplica o modelo para prever a chance de cancelamento em insights
insights["cancel_chance"] = model.predict_proba(insights[[
    "avg_delay", "total_air_time"
]])[:, 1]  # Pega a probabilidade de cancelamento (classe 1)

# --- ETAPA 3: Armazena os Insights no MongoDB ---

# Converte o dataframe em dicionários e insere na nova coleção
insights_records = insights.to_dict("records")
insights_collection.insert_many(insights_records)

print("Insights gravados com sucesso!")