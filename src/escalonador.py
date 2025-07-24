import sys
import classes as c
import socket_utils as su

def FCFS(fila:c.FilaProntas):
    '''Ordena as tarefas presentes em self.fila segundo o algoritmo de priorização First-Come,
    First-Served (FCFS). Nesse algoritmo, as tarefas são atendidas na sequência que elas chegam
    no estado de “pronta”.'''
    pass

def RR(fila:c.FilaProntas):
    '''Ordena as tarefas presentes em self.fila segundo o algoritmo de priorização Round-Robin
    (RR) com quantum fixo de 3 unidades de clock. Nesse algoritmo, as tarefas são atendidas na
    sequência que elas chegam no estado de “pronta”, mas a cada vez que um quantum termina, a
    tarefa volta para a fila de tarefas prontas.'''
    pass

def SJF(fila:c.FilaProntas):
    '''Ordena as tarefas presentes em self.fila segundo o algoritmo de priorização Shortest Job
    First (SJF). Nesse algoritmo, as tarefas são atendidas em ordem crescente de duração
    estimada.'''
    pass

def SRTF(fila:c.FilaProntas):
    '''Ordena as tarefas presentes em self.fila segundo o algoritmo de priorização Shortest
    Remaining Time First (SRTF). Nesse algoritmo, as tarefas são atendidas em ordem crescente
    de duração estimada restante, ou seja, a cada ciclo de clock é feita uma nova comparação
    para definir a tarefa, que tem uma unidade de tempo restante decrementada logo em seguida.'''
    pass

def PRIOc(fila:c.FilaProntas):
    '''Ordena as tarefas presentes em self.fila segundo o algoritmo de priorização por
    prioridades fixas cooperativo (PRIOc). Nesse algoritmo, as tarefas são atendidas em ordem
    crescente de prioridade estática, sem alteração das prioridades ou interrupção de tarefas
    já em processamento.'''
    pass

def PRIOp(fila:c.FilaProntas):
    '''Ordena as tarefas presentes em self.fila segundo o algoritmo de priorização por
    prioridades fixas preemptivo(PRIOp). Nesse algoritmo, as tarefas são atendidas em ordem
    crescente de prioridade estática, com as prioridades não sendo alteradas nunca, porém, a
    cada ciclo de clock, uma nova tarefa que surge com maior prioridade toma o lugar da
    anterior.'''
    pass

def PRIOd(fila:c.FilaProntas):
    '''Ordena as tarefas presentes em self.fila segundo o algoritmo de priorização por
    prioridades dinâmicas (PRIOd). Nesse algoritmo, a cada evento de adição de nova tarefa à
    fila ou encerramento de tarefa, a tarefa com maior prioridade é escolhida. Porém, nesses
    eventos, as tarefas que não foram escalonadas tem sua prioridade aumentada segundo um fator
    de escalonamento a. Além disso, a prioridade dinâmica da tarefa escalonada retrocede à
    prioridade estática. Retorna a tarefa executada neste ciclo de clock'''
    pass

def main(algoritmo:c.Algoritmo):
    '''Implementa o resto'''
    
    PORTA_ESCALONADOR = 4002
    PORTA_CLOCK = 4000
    PORTA_EMISSOR = 4001

    # Inicialização da parte do escalonador, com as coisas necessárias antes de ouvir coisas do clock e emissor e entrar em loop
    
    fila_prontas = c.FilaProntas()
    info_saida = c.InfoSaida()
    

    # Loop e escutando clock e emissor (Enquanto o emissor estiver ativo e a lista de tarefas
    # prontas não estiver vazia, escalona a tarefa do momento)
    # Só passa para o próximo loop quando ouvir o clock
    # Quando o emissor emite, adiciona na fila de prontas
    # Recebe as novas tarefas do emissor + ordena a fila se for necessário + Escalona a Tarefa do momento



    # Finalização,tratamento da saída a partir dos métodos de FilaSaida e  faz os avisos de término
    


    return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Erro: Nenhum algoritmo foi especificado.")
    try:
        algoritmo = c.Algoritmo[sys.argv[1]]
    except KeyError:
        sys.exit("Erro: Algoritmo inválido.")

    main(algoritmo)