"""
Exemplo de uso da biblioteca rdmNames para gerar 10 milhões de nomes.
"""
import time
from datetime import datetime
from pathlib import Path
from tqdm import tqdm
from rdmNames import generate_names_to_file, generate_names

def main():
    # Configuração
    total_names = 10_000_000
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    # Gera um nome de arquivo com timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = output_dir / f"generated_names_{timestamp}.txt"
    
    print(f"Iniciando geração de {total_names:,} nomes...")
    start_time = time.time()
    
    try:
        # Usa a função otimizada para gerar e salvar os nomes
        generate_names_to_file(
            total=total_names,
            output_file=str(output_file),
            batch_size=500_000  # Ajuste o tamanho do lote conforme necessário
        )
        
        # Relatório final
        elapsed = time.time() - start_time
        print("\n" + "="*60)
        print(f"Geração concluída em {elapsed:.2f} segundos")
        print(f"Total de nomes gerados: {total_names:,}")
        print(f"Velocidade média: {total_names/elapsed:,.0f} nomes/segundo")
        print(f"Arquivo gerado: {output_file}")
        print(f"Tamanho do arquivo: {output_file.stat().st_size/1024/1024:.2f} MB")
        print("="*60)
        
    except Exception as e:
        print(f"\nErro durante a geração de nomes: {e}")
    finally:
        print(f"\nTempo total de execução: {time.time() - start_time:.2f} segundos")

if __name__ == "__main__":
    main()
