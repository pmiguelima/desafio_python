#!/usr/bin/env python
import time, os


async def main(file_list):
    pass


if __name__ == "__main__":
    start = time.time()
    print(f"Início: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start))}")
    
    # main(files)
    
    finish = time.time()
    print(f"Fim: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(finish))}")
    print(f"Tempo de execução: {finish - start:.6f} segundos")
    
    