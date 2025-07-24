from socket_utils import send_message
import time

def main():
    PORTA_EMISSOR = 4001
    PORTA_ESCALONADOR = 4002

    clock = 0

    while True:
        send_message(PORTA_EMISSOR, {"tipo": "ciclo", "valor": clock})
        time.sleep(0.005)
        send_message(PORTA_ESCALONADOR, {"tipo": "ciclo", "valor": clock})
        time.sleep(0.095)  # totaliza 100ms
        clock += 1

if __name__ == "__main__":
    
    main()