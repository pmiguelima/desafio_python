import kaggle, os

KAGGLE_OWNER = os.getenv('KAGGLE_OWNER')
KAGGLE_DATASET = os.getenv('KAGGLE_DATASET')

OUTPUT = '/code/data'


def download_dataset():
    kaggle.api.dataset_download_files(f'{KAGGLE_OWNER}/{KAGGLE_DATASET}', path='/code/data', unzip=True)
