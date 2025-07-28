# run.py
import subprocess
import time
import sys
import os

def main():
    if len(sys.argv) < 3:
        print("Uso: python main.py <arquivo_entrada> <algoritmo>")
        sys.exit(1)

    entrada = sys.argv[1]
    algoritmo = sys.argv[2]

    # Caso o arquivo de entrada não seja encontrado
    if not os.path.isfile(entrada):
        print(f"Erro: Arquivo de entrada '{entrada}' não encontrado.")
        sys.exit(1)

    # Caso o algoritmo de escalonamento inserido pelo usuário seja incorreto
    if algoritmo.lower() not in ['fcfs', 'rr', 'sjf', 'srtf', 'prioc', 'priop', 'priod']:
        print("Erro: Algoritmo inválido. Opções: fcfs, rr, sjf, srtf, prioc, priop, priod.")
        sys.exit(1)

    # Inicia Emissor
    print("Iniciando Emissor...")
    emissor = subprocess.Popen(['python', 'emissor.py', entrada])

    time.sleep(1)  # espera emissor subir

    # Inicia Escalonador
    print("Iniciando Escalonador...")
    escalonador = subprocess.Popen(['python', 'escalonador.py', algoritmo])

    time.sleep(1)  # espera escalonador subir

    # Inicia Clock
    print("Iniciando Clock...")
    clock = subprocess.Popen(['python', 'clock.py'])

    # Aguarda os processos terminarem (Clock termina a simulação)
    clock.wait()

    # Encerra os outros processos se ainda estiverem rodando
    escalonador.terminate()
    emissor.terminate()

    print("Todos os processos finalizados.")

if __name__ == "__main__":
    main()