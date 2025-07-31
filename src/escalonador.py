import sys
import time
import classes as c
import socket_utils as socket

def main(algoritmo:c.Algoritmo):
    '''Implementa o resto'''
    
    PORTA_CLOCK = 4000
    PORTA_EMISSOR = 4001
    PORTA_ESCALONADOR = 4002

    # INICIALIZAÇÃO -------------------------------------------------------------------------------

    # Estruturas de controle
    fila_prontas = c.FilaProntas()
    info_saida = c.InfoSaida()
    
    # Estados de controle
    emissao_finalizada = False
    simulacao_ativa = True
    tarefa_executando = None  # Para algoritmos preemptivos
    quantum_atual = 0        # Para Round-Robin

    # IMPLEMENTAÇÃO DOS ALGORITMOS DE ESCALONAMENTO -----------------------------------------------

    def executa_fcfs(clock: int):
        '''Ordena as tarefas presentes em self.fila segundo o algoritmo de priorização First-Come,
        First-Served (FCFS). Nesse algoritmo, as tarefas são atendidas na sequência que elas chegam
        no estado de “pronta”.'''
        pass

    def executa_rr(clock: int):
        '''Ordena as tarefas presentes em self.fila segundo o algoritmo de priorização Round-Robin
        (RR) com quantum fixo de 3 unidades de clock. Nesse algoritmo, as tarefas são atendidas na
        sequência que elas chegam no estado de “pronta”, mas a cada vez que um quantum termina, a
        tarefa volta para a fila de tarefas prontas.'''
        nonlocal quantum_atual, tarefa_executando
        pass

    def executa_sjf(clock: int):
        '''Ordena as tarefas presentes em self.fila segundo o algoritmo de priorização Shortest Job
        First (SJF). Nesse algoritmo, as tarefas são atendidas em ordem crescente de duração
        estimada.'''
        pass

    def executa_srtf(clock: int):
        '''Ordena as tarefas presentes em self.fila segundo o algoritmo de priorização Shortest
        Remaining Time First (SRTF). Nesse algoritmo, as tarefas são atendidas em ordem crescente
        de duração estimada restante, ou seja, a cada ciclo de clock é feita uma nova comparação
        para definir a tarefa, que tem uma unidade de tempo restante decrementada logo em seguida.'''
        pass

    def executa_prioc(clock: int):
        '''Ordena as tarefas presentes em self.fila segundo o algoritmo de priorização por
        prioridades fixas cooperativo (PRIOc). Nesse algoritmo, as tarefas são atendidas em ordem
        crescente de prioridade estática, sem alteração das prioridades ou interrupção de tarefas
        já em processamento.'''
        pass

    def executa_priop(clock: int):
        '''Ordena as tarefas presentes em self.fila segundo o algoritmo de priorização por
        prioridades fixas preemptivo(PRIOp). Nesse algoritmo, as tarefas são atendidas em ordem
        crescente de prioridade estática, com as prioridades não sendo alteradas nunca, porém, a
        cada ciclo de clock, uma nova tarefa que surge com maior prioridade toma o lugar da
        anterior.'''
        pass

    def executa_priod(clock: int):
        '''Ordena as tarefas presentes em self.fila segundo o algoritmo de priorização por
        prioridades dinâmicas (PRIOd). Nesse algoritmo, a cada evento de adição de nova tarefa à
        fila ou encerramento de tarefa, a tarefa com maior prioridade é escolhida. Porém, nesses
        eventos, as tarefas que não foram escalonadas tem sua prioridade aumentada segundo um fator
        de escalonamento a. Além disso, a prioridade dinâmica da tarefa escalonada retrocede à
        prioridade estática. Retorna a tarefa executada neste ciclo de clock'''
        pass

    # Mapeamento dos algoritmos para suas funções
    algoritmos = {
        c.Algoritmo.fcfs: executa_fcfs,
        c.Algoritmo.rr: executa_rr,
        c.Algoritmo.sjf: executa_sjf,
        c.Algoritmo.srtf: executa_srtf,
        c.Algoritmo.prioc: executa_prioc,
        c.Algoritmo.priop: executa_priop,
        c.Algoritmo.priod: executa_priod
    }

    # TRATAMENTO DE MENSAGENS ---------------------------------------------------------------------

    def trata_mensagem(mensagem: dict, addr):
        """Função callback para tratar mensagens recebidas via socket"""
        nonlocal emissao_finalizada
        
        tipo_msg = mensagem.get("tipo")
        
        if tipo_msg == "ciclo":
            # Mensagem do Clock
            clock_atual:int = mensagem.get("valor") # type: ignore 
            print(f"[Escalonador] Clock: {clock_atual}")
            
            # Executa o algoritmo de escalonamento ativo
            funcao_algoritmo = algoritmos[algoritmo]
            funcao_algoritmo(clock_atual)
            
            # Verifica se deve finalizar a simulação
            if emissao_finalizada and fila_prontas.is_empty():
                print("[Escalonador] Todas as tarefas foram concluídas. Finalizando simulação...")
                finalizar_simulacao()
                
        elif tipo_msg == "tarefa":
            # Mensagem do Emissor com nova tarefa
            nova_tarefa = c.Tarefa.from_dict(mensagem)
            print(f"[Escalonador] Nova tarefa recebida: {nova_tarefa.id}")
            fila_prontas.enfilera(nova_tarefa)
            
        elif tipo_msg == "fim_emissao":
            # Mensagem do Emissor indicando que todas as tarefas foram emitidas
            print("[Escalonador] Todas as tarefas foram emitidas pelo Emissor.")
            emissao_finalizada = True
    
    def finalizar_simulacao():
        """Finaliza a simulação, gera arquivo de saída e notifica outros componentes"""
        nonlocal simulacao_ativa
        
        print("[Escalonador] Gerando arquivo de saída...")
        info_saida.gera_saida()
        print("[Escalonador] Arquivo 'saida.txt' gerado com sucesso.")
        
        # Notifica Clock e Emissor sobre o fim da simulação
        print("[Escalonador] Notificando outros componentes sobre fim da simulação...")
        socket.send_message(PORTA_CLOCK, {"tipo": "fim_simulacao"})
        socket.send_message(PORTA_EMISSOR, {"tipo": "fim_simulacao"})
        
        simulacao_ativa = False
        print("[Escalonador] Simulação finalizada.")
        sys.exit(0)

    # LOOP PRINCIPAL ------------------------------------------------------------------------------

    # Inicia o servidor socket para receber mensagens
    socket.start_server(PORTA_ESCALONADOR, trata_mensagem)
    print("[Escalonador] Servidor socket iniciado. Aguardando mensagens...")
    
    # Mantém o processo ativo até a simulação terminar
    while simulacao_ativa:
        time.sleep(0.1)
        
    return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Erro: Nenhum algoritmo foi especificado.")
    try:
        algoritmo = c.Algoritmo[sys.argv[1]]
    except KeyError:
        sys.exit("Erro: Algoritmo inválido.")

    main(algoritmo)