# rdmNames

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Uma biblioteca otimizada para geração de nomes aleatórios em Python, criada por Near Skys.

## 📦 Repositório

Disponível em: [https://github.com/NearSkys/rdmNames](https://github.com/NearSkys/rdmNames)

## Instalação

```bash
pip install -e .
```

## 🚀 Uso Básico

```python
import rdmNames

# Primeiro nome
print(rdmNames.get_first_name())  # Aleatório
print(rdmNames.get_first_name('male'))  # Masculino
print(rdmNames.get_first_name('female'))  # Feminino

# Sobrenome
print(rdmNames.get_last_name())

# Nome completo
print(rdmNames.get_full_name())
```

## ⚡ Geração em Lote (Alta Performance)

```python
from rdmNames import generate_names_to_file, generate_names

# 1. Geração direta para arquivo (recomendado para grandes volumes)
generate_names_to_file(
    total=10_000_000,  # 10 milhões de nomes
    output_file="nomes_10M.txt",
    batch_size=500_000  # Processa em lotes de 500k
)

# 2. Geração em lotes para processamento em memória
for batch in generate_names(total=1_000_000, batch_size=100_000):
    # Cada 'batch' contém 100k nomes
    process_names(batch)
```

## 🎯 Exemplo: Gerar 100 milhões de nomes

```python
# gerar_100_milhoes.py
from rdmNames import generate_names_to_file
from datetime import datetime

total_nomes = 100_000_000
arquivo_saida = f"nomes_100M_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

print(f"Iniciando geração de {total_nomes:,} nomes...")
inicio = datetime.now()

generate_names_to_file(
    total=total_nomes,
    output_file=arquivo_saida,
    batch_size=1_000_000  # 1 milhão por lote
)

tempo_total = (datetime.now() - inicio).total_seconds()
print(f"\nConcluído em {tempo_total:.2f} segundos")
print(f"Velocidade: {total_nomes/tempo_total:,.0f} nomes/segundo")
```

## ✨ Recursos

- ⚡ Geração ultrarrápida (até 500,000 nomes/segundo)
- 💾 Cache em memória para melhor desempenho
- 🧵 Thread-safe
- 🏗️ Tipagem estática
- 🔍 Busca binária eficiente
- 📦 Geração em lote otimizada
- 💾 Suporte a arquivos grandes (milhões de nomes)
- 🔄 Processamento em lotes para economia de memória

## 📋 Requisitos

- Python 3.7+
- NumPy (instalado automaticamente)

## 📄 Licença

MIT License

Copyright (c) 2025 Near Skys

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
