import matplotlib.pyplot as plt
import matplotlib.patches as patches
import sys
from collections import defaultdict
import numpy as np

def parse_output_file(filename):
    """
    Lê o arquivo de saída do escalonador e extrai as informações necessárias.
    
    Args:
        filename (str): Caminho para o arquivo de saída
        
    Returns:
        tuple: (sequencia_execucao, dados_tarefas, tempos_medios)
    """
    with open(filename, 'r') as file:
        lines = file.readlines()
    
    # Primeira linha: sequência de execução
    sequencia_execucao = lines[0].strip().split(';')
    
    # Linhas intermediárias: dados das tarefas
    dados_tarefas = {}
    for i in range(1, len(lines) - 1):
        partes = lines[i].strip().split(';')
        task_id = partes[0]
        ingresso = int(partes[1])
        finalizacao = int(partes[2])
        turnaround = int(partes[3])
        waiting = int(partes[4])
        
        dados_tarefas[task_id] = {
            'ingresso': ingresso,
            'finalizacao': finalizacao,
            'turnaround': turnaround,
            'waiting': waiting
        }
    
    # Última linha: tempos médios
    tempos_medios = lines[-1].strip().split(';')
    turnaround_medio = float(tempos_medios[0])
    waiting_medio = float(tempos_medios[1])
    
    return sequencia_execucao, dados_tarefas, (turnaround_medio, waiting_medio)

def generate_colors(num_tasks):
    """
    Gera cores distintas para cada tarefa.
    
    Args:
        num_tasks (int): Número de tarefas únicas
        
    Returns:
        dict: Mapeamento de tarefa para cor
    """
    colors = plt.cm.tab10(np.linspace(0, 1, num_tasks))
    return colors

def create_gantt_chart(sequencia_execucao, dados_tarefas, tempos_medios, output_filename='gantt_chart.png'):
    """
    Cria o diagrama de Gantt baseado na sequência de execução.
    
    Args:
        sequencia_execucao (list): Lista com a sequência de tarefas executadas
        dados_tarefas (dict): Dicionário com informações das tarefas
        tempos_medios (tuple): Tupla com tempos médios (turnaround, waiting)
        output_filename (str): Nome do arquivo de saída da imagem
    """
    # Identifica todas as tarefas únicas
    tarefas_unicas = list(set(sequencia_execucao))
    tarefas_unicas.sort()  # Ordena para consistência visual
    
    # Gera cores para cada tarefa
    colors = generate_colors(len(tarefas_unicas))
    color_map = {task: colors[i] for i, task in enumerate(tarefas_unicas)}
    
    # Configuração da figura
    fig, ax = plt.subplots(figsize=(max(12, len(sequencia_execucao) * 0.5), 8))
    
    # Altura de cada barra de tarefa
    bar_height = 0.6
    y_positions = {task: i for i, task in enumerate(tarefas_unicas)}
    
    # Primeiro, desenha o período total (chegada até finalização) para cada tarefa
    for task in tarefas_unicas:
        info = dados_tarefas[task]
        ingresso = info['ingresso']
        finalizacao = info['finalizacao']
        
        # Barra de fundo (período total no sistema) - mais clara
        rect_total = patches.Rectangle(
            (ingresso, y_positions[task] - bar_height/2),
            finalizacao - ingresso,  # Duração total no sistema
            bar_height,
            linewidth=1,
            edgecolor='gray',
            facecolor=color_map[task],
            alpha=0.3,  # Mais transparente para mostrar o período total
            hatch='///'  # Padrão para distinguir do tempo de execução
        )
        ax.add_patch(rect_total)
        
        # Adiciona texto indicando o período total
        ax.text(ingresso + (finalizacao - ingresso)/2, y_positions[task] + bar_height/2 + 0.1, 
               f'Total: {finalizacao - ingresso}', 
               ha='center', va='bottom', fontsize=7, style='italic', color='gray')
    
    # Depois, desenha as barras de execução efetiva
    for clock_time, task in enumerate(sequencia_execucao):
        if task:  # Verifica se há uma tarefa executando
            rect = patches.Rectangle(
                (clock_time, y_positions[task] - bar_height/2),
                1,  # Largura de 1 unidade de tempo
                bar_height,
                linewidth=2,
                edgecolor='black',
                facecolor=color_map[task],
                alpha=0.9  # Mais opaco para destacar a execução
            )
            ax.add_patch(rect)
            
            # Adiciona o nome da tarefa no centro da barra de execução
            ax.text(clock_time + 0.5, y_positions[task], task, 
                   ha='center', va='center', fontsize=8, fontweight='bold', color='white')
    
    # Adiciona linhas verticais mostrando chegada e finalização de cada tarefa
    for task in tarefas_unicas:
        info = dados_tarefas[task]
        y_pos = y_positions[task]
        
        # Linha de chegada (verde)
        ax.axvline(x=info['ingresso'], ymin=(y_pos-0.4)/len(tarefas_unicas), 
                  ymax=(y_pos+0.4)/len(tarefas_unicas), color='green', linewidth=2, alpha=0.7)
        ax.text(info['ingresso'], y_pos - bar_height/2 - 0.2, 'Chegada', 
               ha='center', va='top', fontsize=6, color='green', rotation=90)
        
        # Linha de finalização (vermelho)
        ax.axvline(x=info['finalizacao'], ymin=(y_pos-0.4)/len(tarefas_unicas), 
                  ymax=(y_pos+0.4)/len(tarefas_unicas), color='red', linewidth=2, alpha=0.7)
        ax.text(info['finalizacao'], y_pos - bar_height/2 - 0.2, 'Fim', 
               ha='center', va='top', fontsize=6, color='red', rotation=90)
    
    # Configuração dos eixos
    ax.set_xlim(0, len(sequencia_execucao))
    ax.set_ylim(-0.5, len(tarefas_unicas) - 0.5)
    
    # Configuração do eixo X (tempo)
    ax.set_xlabel('Tempo (unidades de clock)', fontsize=12, fontweight='bold')
    ax.set_xticks(range(0, len(sequencia_execucao) + 1, max(1, len(sequencia_execucao) // 20)))
    
    # Configuração do eixo Y (tarefas)
    ax.set_ylabel('Tarefas', fontsize=12, fontweight='bold')
    ax.set_yticks(range(len(tarefas_unicas)))
    ax.set_yticklabels(tarefas_unicas)
    
    # Grade para melhor visualização
    ax.grid(True, axis='x', alpha=0.3, linestyle='--')
    ax.set_axisbelow(True)
    
    # Título
    plt.title('Diagrama de Gantt - Escalonamento de Tarefas', 
              fontsize=16, fontweight='bold', pad=20)
    
    # Adiciona informações estatísticas
    info_text = f'Turnaround Time Médio: {tempos_medios[0]:.1f}\nWaiting Time Médio: {tempos_medios[1]:.1f}'
    ax.text(0.02, 0.98, info_text, transform=ax.transAxes, 
            verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8),
            fontsize=10)
    
    # Adiciona legenda com informações detalhadas das tarefas
    legend_text = "Informações das Tarefas:\n"
    for task in tarefas_unicas:
        info = dados_tarefas[task]
        legend_text += f"{task}: Ingresso={info['ingresso']}, "
        legend_text += f"Finalização={info['finalizacao']}, "
        legend_text += f"Turnaround={info['turnaround']}, "
        legend_text += f"Waiting={info['waiting']}\n"
    
    # Adiciona caixa de texto com informações das tarefas
    ax.text(0.98, 0.02, legend_text.strip(), transform=ax.transAxes,
            verticalalignment='bottom', horizontalalignment='right',
            bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8),
            fontsize=8)
    
    # Ajusta o layout
    plt.tight_layout()
    
    # Salva o diagrama
    plt.savefig(output_filename, dpi=300, bbox_inches='tight')
    print(f"Diagrama de Gantt salvo como: {output_filename}")
    
    # Mostra o diagrama
    plt.show()

def print_execution_summary(sequencia_execucao, dados_tarefas, tempos_medios):
    """
    Imprime um resumo da execução.
    
    Args:
        sequencia_execucao (list): Lista com a sequência de tarefas executadas
        dados_tarefas (dict): Dicionário com informações das tarefas
        tempos_medios (tuple): Tupla com tempos médios
    """
    print("\n" + "="*60)
    print("RESUMO DA EXECUÇÃO DO ESCALONADOR")
    print("="*60)
    
    print(f"Tempo total de execução: {len(sequencia_execucao)} unidades de clock")
    print(f"Número de tarefas: {len(dados_tarefas)}")
    print(f"Turnaround Time médio: {tempos_medios[0]:.1f}")
    print(f"Waiting Time médio: {tempos_medios[1]:.1f}")
    
    print("\nDetalhes das tarefas:")
    print("-" * 60)
    print(f"{'Tarefa':<8} {'Ingresso':<10} {'Finalização':<12} {'Turnaround':<12} {'Waiting':<8}")
    print("-" * 60)
    
    for task_id, info in sorted(dados_tarefas.items()):
        print(f"{task_id:<8} {info['ingresso']:<10} {info['finalizacao']:<12} "
              f"{info['turnaround']:<12} {info['waiting']:<8}")
    
    print("\nSequência de execução:")
    print("-" * 60)
    sequence_str = " -> ".join(sequencia_execucao)
    # Se a sequência for muito longa, quebra em linhas
    if len(sequence_str) > 80:
        for i in range(0, len(sequencia_execucao), 20):
            chunk = sequencia_execucao[i:i+20]
            print(" -> ".join(chunk))
            if i + 20 < len(sequencia_execucao):
                print("   |")
    else:
        print(sequence_str)

def main():
    """
    Função principal do programa.
    """
    if len(sys.argv) != 2:
        print("Uso: python gantt_generator.py <arquivo_saida>")
        print("Exemplo: python gantt_generator.py resultado_fcfs.txt")
        return
    
    filename = sys.argv[1]
    
    try:
        # Lê e processa o arquivo
        sequencia_execucao, dados_tarefas, tempos_medios = parse_output_file(filename)
        
        # Imprime resumo
        print_execution_summary(sequencia_execucao, dados_tarefas, tempos_medios)
        
        # Gera o diagrama de Gantt
        output_name = f"gantt_{filename.replace('.txt', '')}.png"
        create_gantt_chart(sequencia_execucao, dados_tarefas, tempos_medios, output_name)
        
    except FileNotFoundError:
        print(f"Erro: Arquivo '{filename}' não encontrado.")
    except Exception as e:
        print(f"Erro ao processar o arquivo: {e}")

if __name__ == "__main__":
    main()