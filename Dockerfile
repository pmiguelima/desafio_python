FROM python:3.11

ARG KAGGLE_USERNAME
ARG KAGGLE_KEY
ARG KAGGLE_OWNER
ARG KAGGLE_DATASET

ENV PYTHONDONTWRITEBYTECODE=1 \
    CRYPTOGRAPHY_DONT_BUILD_RUST=1 \
    PYTHONUNBUFFERED=1 \
    KAGGLE_USERNAME=$KAGGLE_USERNAME \
    KAGGLE_OWNER=$KAGGLE_OWNER \
    KAGGLE_DATASET=$KAGGLE_DATASET \
    KAGGLE_KEY=$KAGGLE_KEY \
    KAGGLE_ZIP="${KAGGLE_DATASET}.zip"


COPY ./ /code
WORKDIR /code

RUN apt-get update && apt-get install libpq-dev \
    apt-utils \
    unzip \
    g++ \
    gcc -y\ 
    && pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt 
