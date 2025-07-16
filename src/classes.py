from dataclasses import dataclass
from enum import Enum

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

class Criterio(Enum):
    '''Tipo enumerado para ser usado como identificador do citério de ordenação para o método
    ordena da FilaProntas.'''
    duracao = 0
    prioridadeEst = 1
    prioridadeDin = 2

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
        
    def ordena(self, criterio:Criterio):
        '''Ordena a fila segundo um dos determinados atributor de Tarefa indicado por critério.'''
        self.fila.sort(key=lambda t: getattr(t, criterio.name))