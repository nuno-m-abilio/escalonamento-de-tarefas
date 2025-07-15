from dataclasses import dataclass

@dataclass
class Tarefa:
    '''Uma tarefa a ser processada pela simulação. Contém como atributos seu identificador,
    tempo de ingresso, duração prevista e prioridades estática e dinâmica, respectivamente. Obs.:
    quanto menor o valor numérico de prioridade informado, maior a prioridade para execução.'''
    ID:str
    ingresso:int
    duracao:int
    prioridadeEst:int
    prioridadeDin:int

class FilaProntas:
    '''Estrutura que armazena as tarefas que o emissor já informou como prontas por já chegaram a
    seu tempo de ingresso.'''
    def __init__(self):
        '''Inicializa uma lista vazia.'''
        self.fila:list[Tarefa] = []

    def enfilera(self, tarefa:Tarefa):
        '''Adiciona uma Tarefa no fim da fila.'''
        self.fila.append(tarefa)

    def escalona(self) -> Tarefa:
        '''Escalona e retorna a Tarefa do início da fila, finalizando-a caso sua duranção termine.'''
        if self.fila[0].duracao == 1:
            return self.fila.pop(0)
        else:
            self.fila[0].duracao -= 1
            return self.fila[0]
        
    
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