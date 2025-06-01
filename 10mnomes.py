# gerar_100_milhoes.py
from rdmNames import generate_names_to_file
from datetime import datetime

# Configuração
total_nomes = 10_000_000  # 100 milhões de nomes
arquivo_saida = f"nomes_100M_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

print(f"Iniciando geração de {total_nomes:,} nomes...")
inicio = datetime.now()

# Gera e salva os nomes
generate_names_to_file(
    total=total_nomes,
    output_file=arquivo_saida,
    batch_size=1_000_000  # Processa em lotes de 1 milhão
)

# Relatório
tempo_total = (datetime.now() - inicio).total_seconds()
print(f"\nConcluído em {tempo_total:.2f} segundos")
print(f"Velocidade: {total_nomes/tempo_total:,.0f} nomes/segundo")
print(f"Arquivo gerado: {arquivo_saida}")