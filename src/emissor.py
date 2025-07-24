import sys
import os
import classes as c
import socket_utils as su

def main(entrada:str):
    PORTA_ESCALONADOR = 4002
    PORTA_EMISSOR = 4001

    return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Erro: Nenhum arquivo de entrada foi passado.")
    
    entrada = sys.argv[1]
    if not os.path.isfile(entrada):
        sys.exit(f"Erro: O arquivo '{entrada}' não existe ou não é um arquivo válido.")

    main(entrada)
