import socket_utils as socket
import time

def main():
    PORTA_CLOCK = 4000
    PORTA_EMISSOR = 4001
    PORTA_ESCALONADOR = 4002

    clock = 0
    rodando = True

    def trata_mensagem(mensagem: dict, addr):
        nonlocal rodando
        tipo = mensagem.get("tipo")
        if tipo == "fim_simulacao":
            print("[Clock] Recebeu sinal de fim da simulação. Encerrando...")
            rodando = False

    # Inicia o servidor para ouvir mensagens na porta do Clock
    socket.start_server(PORTA_CLOCK, trata_mensagem)

    while rodando:
        socket.send_message(PORTA_EMISSOR, {"tipo": "ciclo", "valor": clock})
        time.sleep(0.005)
        socket.send_message(PORTA_ESCALONADOR, {"tipo": "ciclo", "valor": clock})
        time.sleep(0.095)  # totaliza 100ms
        clock += 1

if __name__ == "__main__":
    
    main()