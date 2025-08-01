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
    tarefa_finalizada_ultimo_clock = False  # Para Round-Robin
    quantum_atual = 3        # Para Round-Robin
    houve_evento_priod = False

    # IMPLEMENTAÇÃO DOS ALGORITMOS DE ESCALONAMENTO -----------------------------------------------

    def executa_fcfs(clock: int):
        '''Ordena as tarefas presentes em self.fila segundo o algoritmo de priorização First-Come,
        First-Served (FCFS). Nesse algoritmo, as tarefas são atendidas na sequência que elas chegam
        no estado de “pronta”.'''
        fila_prontas.escalona(clock, info_saida)

    def executa_rr(clock: int):
        '''Ordena as tarefas presentes em self.fila segundo o algoritmo de priorização Round-Robin
        (RR) com quantum fixo de 3 unidades de clock. Nesse algoritmo, as tarefas são atendidas na
        sequência que elas chegam no estado de “pronta”, mas a cada vez que um quantum termina, a
        tarefa volta para a fila de tarefas prontas.'''
        nonlocal quantum_atual, tarefa_finalizada_ultimo_clock
        QUANTUM = 3
        
        # Se não há tarefas na fila, escalona() vai registrar ciclo vazio
        if fila_prontas.is_empty():
            fila_prontas.escalona(clock, info_saida)
            return None
        
        # Se uma tarefa foi finalizada no último clock ou é o primeiro ciclo, reseta quantum
        if tarefa_finalizada_ultimo_clock or quantum_atual == 0:
            quantum_atual = QUANTUM
            tarefa_finalizada_ultimo_clock = False
        
        # Executa a tarefa usando escalona()
        resultado = fila_prontas.escalona(clock, info_saida)
        quantum_atual -= 1
        
        # Verifica se a tarefa foi finalizada
        if resultado is not None:
            tarefa_id, finalizada = resultado
            if finalizada:
                tarefa_finalizada_ultimo_clock = True
                quantum_atual = 0  # Reset para próxima tarefa
                return None
        
        # Se quantum esgotou e ainda há tarefa executando, faz preempção
        if quantum_atual == 0 and not fila_prontas.is_empty():
            # Move a tarefa atual para o final da fila
            print("PREENPTOU AQUI")
            tarefa_preemptada = fila_prontas.desenfilera()
            fila_prontas.enfilera(tarefa_preemptada)

    def executa_sjf(clock: int):
        '''Ordena as tarefas presentes em self.fila segundo o algoritmo de priorização Shortest Job
        First (SJF). Nesse algoritmo, as tarefas são atendidas em ordem crescente de duração
        estimada.'''
        if not fila_prontas.is_empty():
            tarefa_candidata = fila_prontas.fila[0]
            if tarefa_candidata.duracao_total == tarefa_candidata.duracao_resto:
                fila_prontas.ordena(c.Criterio.duracao_total)
        fila_prontas.escalona(clock, info_saida)


    def executa_srtf(clock: int):
        '''Ordena as tarefas presentes em self.fila segundo o algoritmo de priorização Shortest
        Remaining Time First (SRTF). Nesse algoritmo, as tarefas são atendidas em ordem crescente
        de duração estimada restante, ou seja, a cada ciclo de clock é feita uma nova comparação
        para definir a tarefa, que tem uma unidade de tempo restante decrementada logo em seguida.'''
        fila_prontas.ordena(c.Criterio.duracao_resto)
        fila_prontas.escalona(clock, info_saida)


    def executa_prioc(clock: int):
        '''Ordena as tarefas presentes em self.fila segundo o algoritmo de priorização por
        prioridades fixas cooperativo (PRIOc). Nesse algoritmo, as tarefas são atendidas em ordem
        crescente de prioridade estática, sem alteração das prioridades ou interrupção de tarefas
        já em processamento.'''

        if not fila_prontas.is_empty():
            tarefa_candidata = fila_prontas.fila[0]

            if tarefa_candidata.duracao_resto == tarefa_candidata.duracao_total:
                fila_prontas.ordena(c.Criterio.priod_original)

        fila_prontas.escalona(clock, info_saida)

    def executa_priop(clock: int):
        '''Ordena as tarefas presentes em self.fila segundo o algoritmo de priorização por
        prioridades fixas preemptivo(PRIOp). Nesse algoritmo, as tarefas são atendidas em ordem
        crescente de prioridade estática, com as prioridades não sendo alteradas nunca, porém, a
        cada ciclo de clock, uma nova tarefa que surge com maior prioridade toma o lugar da
        anterior.'''

        fila_prontas.ordena(c.Criterio.priod_original)
        fila_prontas.escalona(clock, info_saida)

    def executa_priod(clock: int):
        '''Ordena as tarefas presentes em self.fila segundo o algoritmo de priorização por
        prioridades dinâmicas (PRIOd). Nesse algoritmo, a cada evento de adição de nova tarefa à
        fila ou encerramento de tarefa, a tarefa com maior prioridade é escolhida. Porém, nesses
        eventos, as tarefas que não foram escalonadas tem sua prioridade aumentada segundo um fator
        de escalonamento a. Além disso, a prioridade dinâmica da tarefa escalonada retrocede à
        prioridade estática. Retorna a tarefa executada neste ciclo de clock'''
        nonlocal houve_evento_priod
        
        FATOR_ENVELHECIMENTO = 1
        
        # Se não há tarefas na fila, escalona() vai registrar ciclo vazio
        if fila_prontas.is_empty():
            fila_prontas.escalona(clock, info_saida)
            return
        
        # Se houve evento (nova tarefa ou tarefa finalizada), aplica regras PRIOd
        if houve_evento_priod:
            
            # 1. Escolhe a tarefa com maior prioridade dinâmica (menor valor numérico)
            fila_prontas.ordena(c.Criterio.priod_dinamica)
            tarefa_escolhida = fila_prontas.fila[0]
            
            # 2. Tarefas NÃO escalonadas têm prioridade melhorada (aging)
            for tarefa in fila_prontas.fila:
                if tarefa != tarefa_escolhida:
                    # Melhora prioridade (diminui valor) respeitando limite mínimo de 1
                    tarefa.priod_dinamica = max(1, tarefa.priod_dinamica - FATOR_ENVELHECIMENTO)
            
            # 3. Tarefa escalonada retrocede à prioridade estática
            tarefa_escolhida.priod_dinamica = tarefa_escolhida.priod_original
        
        # Executa a tarefa com maior prioridade dinâmica
        resultado = fila_prontas.escalona(clock, info_saida)
        
        # Se uma tarefa foi finalizada, marca evento para próximo ciclo
        if resultado is not None:
            tarefa_id, finalizada = resultado
            if finalizada:
                houve_evento_priod = True

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
        nonlocal emissao_finalizada, houve_evento_priod
        
        tipo_msg = mensagem.get("tipo")
        
        if tipo_msg == "ciclo":
            # Mensagem do Clock
            clock_atual:int = mensagem.get("valor") # type: ignore 
            print(f"[Escalonador] Clock: {clock_atual}")
            
            # Executa o algoritmo de escalonamento ativo
            funcao_algoritmo = algoritmos[algoritmo]
            funcao_algoritmo(clock_atual)
            
            # Reset das flags após processar o ciclo
            houve_evento_priod = False
            
            # Verifica se deve finalizar a simulação
            if emissao_finalizada and fila_prontas.is_empty():
                print("[Escalonador] Todas as tarefas foram concluídas. Finalizando simulação...")
                finalizar_simulacao()
                
        elif tipo_msg == "tarefa":
            # Mensagem do Emissor com nova tarefa
            nova_tarefa = c.Tarefa.from_dict(mensagem)
            print(f"[Escalonador] Nova tarefa recebida: {nova_tarefa.id}")
            fila_prontas.enfilera(nova_tarefa)
            houve_evento_priod = True
            
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