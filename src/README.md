# Sistema de Escalonamento de Tarefas - Código Fonte

## Descrição

Este diretório contém a implementação do sistema de simulação de algoritmos de escalonamento de tarefas para a disciplina de Sistemas Operacionais. O sistema é composto por três processos independentes que se comunicam via sockets TCP.

## Requisitos

- Python 3.x
- Sistema operacional: Windows 10+, Linux (kernel 2022+) ou macOS 14+
- Arquivo de entrada no formato especificado

## Estrutura dos Arquivos

- `main.py` - Ponto de entrada e orquestrador dos processos
- `clock.py` - Componente Clock (simulador de tempo)
- `emissor.py` - Emissor de Tarefas
- `escalonador.py` - Escalonador de Tarefas
- `classes.py` - Estruturas de dados e classes base
- `socket_utils.py` - Utilitários para comunicação via sockets
- `entrada00.txt` - Arquivo de exemplo com tarefas

## Formato do Arquivo de Entrada

O arquivo de entrada deve conter uma tarefa por linha, seguindo o formato:
```
ID;tempo_de_ingresso;duracao_prevista;prioridade
```

Exemplo:
```
t0;0;5;1
t1;1;3;2
t2;3;4;1
```

**Nota:** Quanto menor o valor numérico da prioridade, maior a prioridade de execução.

## Como Executar

### Comando Básico
```bash
python main.py <arquivo_entrada> <algoritmo>
```

### Algoritmos Disponíveis
- `fcfs` - First-Come, First-Served
- `rr` - Round-Robin (quantum = 3)
- `sjf` - Shortest Job First
- `srtf` - Shortest Remaining Time First
- `prioc` - Prioridades fixas cooperativo
- `priop` - Prioridades fixas preemptivo
- `priod` - Prioridades dinâmicas

### Exemplos de Uso
```bash
# Executar FCFS com arquivo de exemplo
python main.py entrada00.txt fcfs

# Executar Round-Robin
python main.py entrada00.txt rr

# Executar com arquivo personalizado
python main.py meu_arquivo.txt sjf
```

## Arquivo de Saída

Após a execução, será gerado o arquivo `saida.txt` contendo:
1. Sequência de tarefas escalonadas por ciclo de clock
2. Dados individuais de cada tarefa (ID, ingresso, finalização, turnaround time, waiting time)
3. Médias de turnaround time e waiting time

## Funcionamento

1. O `main.py` valida os parâmetros e inicia os três processos na ordem correta
2. O **Emissor** carrega as tarefas e aguarda sinais do Clock
3. O **Escalonador** prepara as estruturas de dados e aguarda tarefas
4. O **Clock** inicia a simulação enviando sinais síncronos
5. A simulação termina quando todas as tarefas são concluídas
6. O arquivo de saída é gerado automaticamente

## Resolução de Problemas

- **Erro "Arquivo não encontrado"**: Verifique se o arquivo de entrada existe no diretório atual
- **Erro "Algoritmo inválido"**: Use um dos algoritmos listados acima
- **Processo não finaliza**: Use Ctrl+C para interromper e tente novamente
- **Erro de porta em uso**: Aguarde alguns segundos e execute novamente