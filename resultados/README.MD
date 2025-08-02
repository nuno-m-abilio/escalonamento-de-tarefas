# Sistema de Escalonamento - Resultados e Visualização

## Descrição

Este diretório contém as ferramentas para geração de gráficos de Gantt e os resultados das simulações dos algoritmos de escalonamento. O gerador de diagramas permite visualizar graficamente o comportamento temporal de cada algoritmo implementado.

## Estrutura dos Arquivos

- `gantt_generator.py` - Gerador de diagramas de Gantt
- `gantt_saida_*.png` - Diagramas de Gantt gerados para cada algoritmo
- `saida_*.txt` - Arquivos de saída das simulações para cada algoritmo

## Pré-requisitos

Antes de executar o gerador de diagramas, instale as dependências necessárias:

```bash
pip install matplotlib numpy
```

**Nota:** Após a instalação, ferramentas como mypy podem exibir warnings sobre tipagem, mas isso não afeta o funcionamento do programa.

## Como Usar o Gerador de Diagramas

### 1. Copiar Arquivo de Saída

Primeiro, copie o arquivo `saida.txt` gerado na pasta `src/` para esta pasta `resultados/`:

```bash
# No diretório do projeto
cp src/saida.txt resultados/saida_algoritmo.txt
```

### 2. Executar o Gerador

```bash
python gantt_generator.py <arquivo_saida>
```

### Exemplos de Uso

```bash
# Gerar diagrama para FCFS
python gantt_generator.py saida_fcfs.txt

# Gerar diagrama para Round-Robin
python gantt_generator.py saida_rr.txt

# Gerar diagrama para SJF
python gantt_generator.py saida_sjf.txt
```

## Funcionalidades do Gerador

O `gantt_generator.py` oferece:

### 1. **Análise Textual**
- Resumo completo da execução
- Métricas de desempenho (turnaround time e waiting time)
- Detalhes individuais de cada tarefa
- Sequência temporal de execução

### 2. **Diagrama de Gantt Visual**
- **Barras de execução**: Mostram quando cada tarefa está efetivamente utilizando a CPU
- **Períodos totais**: Indicam o tempo total que cada tarefa permaneceu no sistema
- **Marcadores temporais**: Linhas verdes (chegada) e vermelhas (finalização)
- **Cores distintas**: Cada tarefa possui uma cor única para fácil identificação
- **Informações estatísticas**: Tempos médios exibidos no canto superior esquerdo
- **Detalhes das tarefas**: Informações completas no canto inferior direito

### 3. **Arquivo de Imagem**
- Salva automaticamente como `gantt_<nome_arquivo>.png`
- Alta resolução (300 DPI)
- Formato otimizado para relatórios

## Interpretação do Diagrama

### Elementos Visuais

- **Barras sólidas coloridas**: Tempo de execução efetiva da tarefa na CPU
- **Barras tracejadas transparentes**: Tempo total da tarefa no sistema (chegada → finalização)
- **Linha verde vertical**: Momento de chegada da tarefa
- **Linha vermelha vertical**: Momento de finalização da tarefa
- **Grade pontilhada**: Facilita a leitura temporal

### Métricas Apresentadas

- **Turnaround Time**: Tempo total desde a chegada até a finalização
- **Waiting Time**: Tempo que a tarefa aguardou na fila (Turnaround - Duração)
- **Tempos médios**: Média aritmética de todas as tarefas

## Exemplo de Saída

Ao executar o gerador, você verá:

```
============================================================
RESUMO DA EXECUÇÃO DO ESCALONADOR
============================================================
Tempo total de execução: 15 unidades de clock
Número de tarefas: 4
Turnaround Time médio: 8.5
Waiting Time médio: 3.2

Detalhes das tarefas:
------------------------------------------------------------
Tarefa   Ingresso   Finalização  Turnaround   Waiting
------------------------------------------------------------
t0       0          5            5            0
t1       1          10           9            6
t2       3          12           9            5
t3       4          15           11           7

Sequência de execução:
------------------------------------------------------------
t0 -> t0 -> t0 -> t0 -> t0 -> t1 -> t1 -> t1 -> t2 -> t2 -> t2 -> t2 -> t3 -> t3 -> t3

Diagrama de Gantt salvo como: gantt_saida_fcfs.png
```

## Resultados Disponíveis

Este diretório contém os resultados pré-gerados para todos os algoritmos:

- **FCFS**: `saida_fcfs.txt` e `gantt_saida_fcfs.png`
- **Round-Robin**: `saida_rr.txt` e `gantt_saida_rr.png`
- **SJF**: `saida_sjf.txt` e `gantt_saida_sjf.png`
- **SRTF**: `saida_srtf.txt` e `gantt_saida_srtf.png`
- **PRIOc**: `saida_prioc.txt` e `gantt_saida_prioc.png`
- **PRIOp**: `saida_priop.txt` e `gantt_saida_priop.png`
- **PRIOd**: `saida_priod.txt` e `gantt_saida_priod.png`

## Resolução de Problemas

- **Erro "Module not found"**: Execute `pip install matplotlib numpy`
- **Warnings do mypy**: Pode ignorar, não afeta a execução
- **Arquivo não encontrado**: Verifique se copiou o arquivo de saída corretamente
- **Imagem não abre**: Verifique se possui um visualizador de imagens PNG instalado
- **Gráfico muito pequeno**: O tamanho se ajusta automaticamente ao número de tarefas e tempo total

## Dicas de Uso

1. **Compare algoritmos**: Gere diagramas para diferentes algoritmos e compare visualmente
2. **Analise métricas**: Use os tempos médios para avaliar eficiência
3. **Observe padrões**: Identifique características como preempção, starvation e fairness
4. **Documente resultados**: Use as imagens geradas em relatórios e apresentações