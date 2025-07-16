



def FCFS(self):
    '''Ordena as tarefas presentes em self.fila segundo o algoritmo de priorização First-Come,
    First-Served (FCFS). Nesse algoritmo, as tarefas são atendidas na sequência que elas chegam
    no estado de “pronta”.'''
    pass

def RR(self):
    '''Ordena as tarefas presentes em self.fila segundo o algoritmo de priorização Round-Robin
    (RR) com quantum fixo de 3 unidades de clock. Nesse algoritmo, as tarefas são atendidas na
    sequência que elas chegam no estado de “pronta”, mas a cada vez que um quantum termina, a
    tarefa volta para a fila de tarefas prontas.'''
    pass

def SJF(self):
    '''Ordena as tarefas presentes em self.fila segundo o algoritmo de priorização Shortest Job
    First (SJF). Nesse algoritmo, as tarefas são atendidas em ordem crescente de duração
    estimada.'''
    pass

def SRTF(self):
    '''Ordena as tarefas presentes em self.fila segundo o algoritmo de priorização Shortest
    Remaining Time First (SRTF). Nesse algoritmo, as tarefas são atendidas em ordem crescente
    de duração estimada restante, ou seja, a cada ciclo de clock é feita uma nova comparação
    para definir a tarefa, que tem uma unidade de tempo restante decrementada logo em seguida.'''
    pass

def PRIOc(self):
    '''Ordena as tarefas presentes em self.fila segundo o algoritmo de priorização por
    prioridades fixas cooperativo (PRIOc). Nesse algoritmo, as tarefas são atendidas em ordem
    crescente de prioridade estática, sem alteração das prioridades ou interrupção de tarefas
    já em processamento.'''
    pass

def PRIOp(self):
    '''Ordena as tarefas presentes em self.fila segundo o algoritmo de priorização por
    prioridades fixas preemptivo(PRIOp). Nesse algoritmo, as tarefas são atendidas em ordem
    crescente de prioridade estática, com as prioridades não sendo alteradas nunca, porém, a
    cada ciclo de clock, uma nova tarefa que surge com maior prioridade toma o lugar da
    anterior.'''
    pass

def PRIOd(self):
    '''Ordena as tarefas presentes em self.fila segundo o algoritmo de priorização por
prioridades dinâmicas (PRIOd). Nesse algoritmo, a cada evento de adição de nova tarefa à
fila ou encerramento de tarefa, a tarefa com maior prioridade é escolhida. Porém, nesses
eventos, as tarefas que não foram escalonadas tem sua prioridade aumentada segundo um fator
de escalonamento a. Além disso, a prioridade dinâmica da tarefa escalonada retrocede à
prioridade estática'''
    pass