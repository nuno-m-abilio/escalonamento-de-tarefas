import sys
import os
import classes as c
import socket_utils as socket
import time

def main(entrada):

    PORTA_EMISSOR = 4001
    PORTA_ESCALONADOR = 4002

    # Tarefas que foram lidas do arquivo mas ainda não foram enviadas ao escalonador
    # É declarada globalmente para ser acessível pela função de callback do socket.
    tarefas_agendadas = []

    # Indica se todas as tarefas foram emitidas
    emissao_finalizada = False

    def carregar_tarefas(entrada: str) -> list[c.Tarefa]:
        '''Abre o arquivo de entrada para leitura, organiza as tarefas em classes e as adicona em uma pré-lista'''
        tarefas = []

        with open(entrada, 'r') as arquivo:
            for linha in arquivo:
                linha = linha.strip()
                partes = linha.split(";")

                tarefa = c.Tarefa(
                    id=partes[0],
                    ingresso=int(partes[1]),
                    duracao=int(partes[2]),
                    prioridade=int(partes[3])
                )
                tarefas.append(tarefa)

        return tarefas

    def trata_mensagem(mensagem: dict, addr):
        '''
        Função de callback que será executada toda vez que o Emissor receber uma mensagem via socket.
        É o coração da lógica do Emissor.
        '''
        nonlocal tarefas_agendadas, emissao_finalizada

        # O Emissor espera dois tipos de mensagem: um ciclo do clock ou o fim da simulação
        tipo_msg = mensagem.get("tipo")

        # Caso a mensagem recebida seja de ciclo de clock:
        if tipo_msg == "ciclo":
            clock_atual = mensagem.get("valor")
            print(f"[Emissor] Recebeu ciclo de clock: {clock_atual}")

            # Cria uma lista de tarefas que estão prontas para serem enviadas neste ciclo
            tarefas_prontas = []
            for tarefa in tarefas_agendadas:
                if tarefa.ingresso == clock_atual:
                    tarefas_prontas.append(tarefa)

            for tarefa in tarefas_prontas:
                # Converte o objeto Tarefa para um dicionário para ser enviado
                msg_tarefa = c.Tarefa.to_dict(tarefa)
                print(f"[Emissor] Tarefa '{tarefa.id}' pronta. Enviando para o Escalonador.")
                socket.send_message(PORTA_ESCALONADOR, msg_tarefa)
                # Remove a tarefa da lista de agendadas após o envio
                tarefas_agendadas.remove(tarefa)

            # Após verificar todas as tarefas, checa se a lista de agendadas está vazia
            # e se a notificação de fim de emissão ainda não foi enviada. 
            if not tarefas_agendadas and not emissao_finalizada:
                print("[Emissor] Todas as tarefas foram emitidas. Notificando o Escalonador.")
                socket.send_message(PORTA_ESCALONADOR, {"tipo": "fim_emissao"})
                emissao_finalizada = True

        # Caso a mensagem recebida seja de fim da simulação:
        elif tipo_msg == "fim_simulacao":
            # Mensagem recebida do Escalonador para encerrar o processo 
            print("[Emissor] Recebeu sinal de fim da simulação. Encerrando...")
            sys.exit(0)

    tarefas_agendadas = carregar_tarefas(entrada)
    print(f"[Emissor] {len(tarefas_agendadas)} tarefas carregadas do arquivo '{entrada}'.")

    # Inicia o servidor socket em uma thread separada para ouvir mensagens na sua porta.
    # A função `handle_message` será chamada para cada mensagem recebida.
    socket.start_server(PORTA_EMISSOR, trata_mensagem)

    # Mantém o processo principal vivo para que a thread do servidor possa continuar rodando.
    # O processo terminará quando `sys.exit(0)` for chamado em `handle_message`.
    while True:
        time.sleep(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Erro: Nenhum arquivo de entrada foi passado.")
    
    entrada = sys.argv[1]
    if not os.path.isfile(entrada):
        sys.exit(f"Erro: O arquivo '{entrada}' não existe ou não é um arquivo válido.")

    main(entrada)
