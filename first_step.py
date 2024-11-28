#!/usr/bin/env python
import time, os

from src.extract.downloader import OUTPUT, download_dataset
from src.transform.process import parallel_file_execution


BASE_DIR = OUTPUT


def main(file_list):
    parallel_file_execution(file_list, chunk_size=10000, max_workers=6)


if __name__ == "__main__":
    start = time.time()
    print(f"Início: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start))}")
    
    #download_dataset()
    
    files = [f'{BASE_DIR}/{item}' for item in os.listdir(BASE_DIR)]
    
    main(files)
    
    finish = time.time()
    print(f"Fim: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(finish))}")
    print(f"Tempo de execução: {((finish - start)/60):.6f} minutos")
    
    