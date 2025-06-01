#!/usr/bin/env python3
"""
Script ultra rápido para gerar milhões de nomes aleatórios.
"""
import time
import random
import logging
import os
from datetime import datetime, timedelta
from typing import List
import numpy as np
from tqdm import tqdm

# Desabilitar logs para melhor performance
logging.disable(logging.CRITICAL)

# Constantes otimizadas
TOTAL_NAMES = 10_000_000  # 10 milhões de nomes
BATCH_SIZE = 100_000     # Tamanho do lote para escrita em arquivo
LOG_INTERVAL = 1_000_000 # Log a cada 1 milhão de nomes
BUFFER_SIZE = 10_000     # Tamanho do buffer para escrita em arquivo

# Carregar dados uma única vez
FIRST_NAMES = []
LAST_NAMES = []

def load_names():
    """Carrega os nomes uma única vez na memória."""
    global FIRST_NAMES, LAST_NAMES
    
    # Carrega nomes masculinos
    with open('rdmNames/data/dist.male.first', 'r', encoding='utf-8') as f:
        male_names = [line.split()[0].capitalize() for line in f]
    
    # Carrega nomes femininos
    with open('rdmNames/data/dist.female.first', 'r', encoding='utf-8') as f:
        female_names = [line.split()[0].capitalize() for line in f]
    
    # Combina nomes masculinos e femininos
    FIRST_NAMES = male_names + female_names
    
    # Carrega sobrenomes
    with open('rdmNames/data/dist.all.last', 'r', encoding='utf-8') as f:
        LAST_NAMES = [line.split()[0].capitalize() for line in f]

# Carregar dados ao importar
load_names()

def generate_name_batch(batch_size: int) -> List[str]:
    """Gera um lote de nomes completos de forma otimizada."""
    firsts = np.random.choice(FIRST_NAMES, size=batch_size)
    lasts = np.random.choice(LAST_NAMES, size=batch_size)
    return [f"{first} {last}" for first, last in zip(firsts, lasts)]

def save_names_to_file(names: List[str], filename: str) -> None:
    """Salva uma lista de nomes em um arquivo de forma otimizada."""
    with open(filename, 'a', encoding='utf-8', buffering=BUFFER_SIZE) as f:
        f.write('\n'.join(names) + '\n')

def generate_names(total: int, batch_size: int) -> None:
    """Gera nomes de forma otimizada."""
    # Cria o diretório de saída se não existir
    os.makedirs('output', exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f'output/generated_names_{timestamp}.txt'
    
    # Cria o arquivo vazio
    open(output_file, 'w').close()
    
    start_time = time.time()
    total_generated = 0
    
    # Usando tqdm para barra de progresso
    with tqdm(total=total, desc="Gerando nomes", unit="nomes") as pbar:
        remaining = total
        
        while remaining > 0:
            current_batch = min(batch_size, remaining)
            
            # Gera e salva o lote
            names = generate_name_batch(current_batch)
            save_names_to_file(names, output_file)
            
            # Atualiza contadores
            remaining -= current_batch
            total_generated += current_batch
            pbar.update(current_batch)
            
            # Log de progresso
            if total_generated % LOG_INTERVAL == 0:
                elapsed = time.time() - start_time
                print(f"\nGerados {total_generated:,} nomes em {elapsed:.2f} segundos")
                print(f"Velocidade: {total_generated/elapsed:,.0f} nomes/segundo")
                
                if total_generated > 0:
                    remaining_time = (elapsed / total_generated) * (total - total_generated)
                    print(f"Tempo estimado restante: {timedelta(seconds=int(remaining_time))}")
    
    # Relatório final
    elapsed = time.time() - start_time
    print("\n" + "="*60)
    print(f"Geração concluída em {elapsed:.2f} segundos")
    print(f"Total de nomes gerados: {total_generated:,}")
    print(f"Velocidade média: {total_generated/elapsed:,.0f} nomes/segundo")
    print(f"Arquivo gerado: {output_file}")
    print(f"Tamanho do arquivo: {os.path.getsize(output_file)/1024/1024:.2f} MB")
    print("="*60)

def main():
    """Função principal."""
    print(f"Iniciando geração de {TOTAL_NAMES:,} nomes...")
    print("Otimizações ativadas:")
    print("- Geração em lote otimizada")
    print(f"- Tamanho do lote: {BATCH_SIZE:,} nomes")
    print(f"- Buffer de escrita: {BUFFER_SIZE/1024:.1f}KB")
    print("-" * 50)
    
    start_time = time.time()
    
    try:
        generate_names(TOTAL_NAMES, BATCH_SIZE)
    except KeyboardInterrupt:
        print("\nProcesso interrompido pelo usuário.")
    except Exception as e:
        print(f"\nErro durante a geração de nomes: {str(e)}")
    finally:
        elapsed = time.time() - start_time
        print(f"\nTempo total de execução: {elapsed:.2f} segundos")

if __name__ == "__main__":
    # Verifica se o numpy está instalado
    try:
        import numpy as np
    except ImportError:
        print("Instalando NumPy para melhor desempenho...")
        import subprocess
        import sys
        subprocess.check_call([sys.executable, "-m", "pip", "install", "numpy"])
        import numpy as np
    
    main()
