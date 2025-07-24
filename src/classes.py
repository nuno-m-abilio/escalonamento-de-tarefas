from enum import Enum

class Tarefa:
    '''Uma tarefa a ser processada pela simulação. Contém como atributos seu identificador,
    tempo de ingresso, duração total prevista, duração previsa no momento, prioridades original e
    no momento e tempos iniciais e finais de execução. Obs.: quanto menor o valor numérico de
    prioridade informado, maior a prioridade para execução.'''
    
    def __init__(self, id:str, ingresso:int, duracao:int, prioridade:int):
        '''Construtor da classe.'''
        self.id:str = id
        self.ingresso:int = ingresso
        self.duracao_total:int = duracao
        self.duracao_resto:int = duracao
        self.priod_original:int = prioridade
        self.priod_dinamica:int = prioridade
        self.inicio_exe:int|None = None
        self.fim_exe:int|None = None

    def to_dict(self) -> dict:
        '''Serializa a tarefa para um dicionário compatível com JSON.'''
        return {
            "tipo": "tarefa",
            "id": self.id,
            "ingresso": self.ingresso,
            "duracao": self.duracao_total,
            "prioridade": self.priod_original,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Tarefa":
        '''Cria uma instância de Tarefa a partir de um dicionário.'''
        return cls(
            id=data["id"],
            ingresso=data["ingresso"],
            duracao=data["duracao"],
            prioridade=data["prioridade"]
        )

class Algoritmo(Enum):
    '''Tipo do algoritmo de priorização em execução.'''
    fcfs = 0
    rr = 1
    sjf = 2
    srtf = 3
    prioc = 4
    priop = 5
    priod = 6

class Criterio(Enum):
    '''Tipo enumerado para ser usado como identificador do citério de ordenação para o método
    ordena da FilaProntas.'''
    duracao = 0
    priod_original = 1
    priod_dinamica = 2

class InfoSaida:
    '''Estrutura que armazena as tarefas que foram concluídas na simulação e os ids das tarefas
    executadas a cada ciclo de clock, além de implementar os métodos para escrever o arquivo de
    saída com os dados da execução.'''
    def __init__(self) -> None:
        '''Inicializa ambas as listas como vazias.'''
        self.tarefas_concluidas:list[Tarefa] = []
        self.id_por_clock:list[str|None] = []
    
    def finaliza_tarefa(self, tarefa:Tarefa):
        '''Adiciona uma Tarefa no fim da lista de tarefas concluídas.'''
        self.tarefas_concluidas.append(tarefa)

    def add_id_do_clock(self, id=None):
        '''Adiciona o id do armunento na lista de id de tarefas por ciclo de clock. Caso neste
        ciclo de clock não tenham tarefas sendo executadas, chame a função sem argumentos que None
        será adicionado.'''
        self.id_por_clock.append(id)

class FilaProntas:
    '''Estrutura que armazena as tarefas que o emissor já informou como prontas por já chegarem ao
    seu tempo de ingresso.'''
    def __init__(self) -> None:
        '''Inicializa uma lista vazia.'''
        self.fila:list[Tarefa] = []

    def enfilera(self, tarefa:Tarefa):
        '''Adiciona uma Tarefa no fim da fila.'''
        self.fila.append(tarefa)

    def desenfilera(self):
        '''Retira e retorna a primeira tarefa da fila.'''
        return self.fila.pop(0)

    def escalona(self, clock:int, info_saida:InfoSaida) -> tuple[str, bool]|None:
        '''Escalona a tarefa do inicio da fila e retorna seu id (junto a um bool que indica se a
        tarefa foi finalizada) caso a lista não estiver vazia. Caso contrário, retorna None. Todos
        os dados de saída são atualizados em info_saida.'''
        if not self.fila:
            info_saida.add_id_do_clock()
            return None
        else:
            tarefa:Tarefa = self.fila[0]
            if tarefa.duracao_resto == tarefa.duracao_total:
                tarefa.inicio_exe = clock
            tarefa.duracao_resto -= 1
            tarefa_id = tarefa.id
            info_saida.add_id_do_clock(tarefa_id)
            if tarefa.duracao_resto == 0:
                tarefa.fim_exe = clock
                info_saida.finaliza_tarefa(self.fila.pop(0))
                return tarefa_id, True
            return tarefa_id, False
           
        
    def ordena(self, criterio:Criterio):
        '''Ordena a fila segundo um dos determinados atributor de Tarefa indicado por critério.'''
        self.fila.sort(key=lambda t: getattr(t, criterio.name))
    
    def is_empty(self):
        '''Retorna True Caso a fila esteja vazia e False caso contrário.'''
        return not self.fila