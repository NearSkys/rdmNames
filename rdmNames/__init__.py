"""
rdmNames - Uma biblioteca otimizada para geração de nomes aleatórios.

Esta versão inclui otimizações de desempenho como cache em memória,
busca binária e suporte a concorrência.
"""
from __future__ import annotations
import os
import bisect
import random
import threading
import numpy as np
from os.path import abspath, join, dirname, exists
from typing import Dict, List, Optional, Tuple, Union, TypeVar, Generic, Any, Generator

__version__ = '1.0.0'
__author__ = 'Seu Nome'
__license__ = 'MIT'

# Type aliases
T = TypeVar('T')
NameData = List[Tuple[str, float]]

# Cache global thread-safe
class _NameCache:
    _instance = None
    _lock = threading.RLock()
    
    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._cache: Dict[str, NameData] = {}
            return cls._instance
    
    def get(self, filename: str) -> Optional[NameData]:
        with self._lock:
            return self._cache.get(filename)
    
    def set(self, filename: str, data: NameData) -> None:
        with self._lock:
            self._cache[filename] = data

# Inicialização do cache
_name_cache = _NameCache()

def _get_full_path(filename: str) -> str:
    """Retorna o caminho absoluto para um arquivo de dados."""
    return abspath(join(dirname(__file__), 'data', filename))

# Mapeamento de arquivos
FILES = {
    'first:male': _get_full_path('dist.male.first'),
    'first:female': _get_full_path('dist.female.first'),
    'last': _get_full_path('dist.all.last'),
}

def _load_names(filename: str) -> NameData:
    """Carrega e armazena em cache os nomes do arquivo."""
    # Verifica se já está em cache
    if cached := _name_cache.get(filename):
        return cached
    
    # Carrega do arquivo se não estiver em cache
    names: NameData = []
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) >= 3:
                    name = parts[0]
                    cummulative = float(parts[2])
                    names.append((name, cummulative))
        
        # Ordena por probabilidade acumulada para busca binária
        names.sort(key=lambda x: x[1])
        
        # Armazena no cache
        _name_cache.set(filename, names)
        return names
    except Exception as e:
        raise RuntimeError(f"Falha ao carregar o arquivo {filename}: {str(e)}")

def _get_random_name(names: NameData) -> str:
    """Obtém um nome aleatório usando busca binária."""
    if not names:
        return ""
    
    # Gera um valor aleatório e usa busca binária para encontrar o nome
    target = random.random() * 90
    
    # Extrai apenas os valores acumulados para busca binária
    cumulatives = [c for _, c in names]
    
    # Encontra o índice usando busca binária
    idx = bisect.bisect_right(cumulatives, target)
    
    # Retorna o nome correspondente, ou o último se o índice for maior que o tamanho
    return names[min(idx, len(names) - 1)][0]

def get_first_name(gender: Optional[str] = None) -> str:
    """Retorna um primeiro nome aleatório."""
    if gender not in ('male', 'female'):
        gender = random.choice(('male', 'female'))
    
    filename = FILES[f'first:{gender}']
    names = _load_names(filename)
    return _get_random_name(names).capitalize()

def get_last_name() -> str:
    """Retorna um sobrenome aleatório."""
    filename = FILES['last']
    names = _load_names(filename)
    return _get_random_name(names).capitalize()

def get_full_name(gender: Optional[str] = None) -> str:
    """Retorna um nome completo aleatório."""
    return f"{get_first_name(gender)} {get_last_name()}"

# Otimização: Pré-carrega os dados na primeira importação
# Isso garante que o carregamento ocorra apenas uma vez
_ = _load_names(FILES['last'])
_ = _load_names(FILES['first:male'])
_ = _load_names(FILES['first:female'])

# Carrega todos os nomes em listas para acesso rápido
FIRST_NAMES = []
LAST_NAMES = []

def _load_all_names() -> None:
    """Carrega todos os nomes em listas para acesso rápido."""
    global FIRST_NAMES, LAST_NAMES
    
    # Carrega nomes masculinos
    male_names = []
    with open(FILES['first:male'], 'r', encoding='utf-8') as f:
        male_names = [line.split()[0].capitalize() for line in f]
    
    # Carrega nomes femininos
    female_names = []
    with open(FILES['first:female'], 'r', encoding='utf-8') as f:
        female_names = [line.split()[0].capitalize() for line in f]
    
    # Carrega sobrenomes
    with open(FILES['last'], 'r', encoding='utf-8') as f:
        LAST_NAMES = [line.split()[0].capitalize() for line in f]
    
    # Combina nomes masculinos e femininos
    FIRST_NAMES = male_names + female_names

# Carrega todos os nomes na inicialização
_load_all_names()

def generate_names_batch(batch_size: int = 100_000) -> List[str]:
    """
    Gera um lote de nomes completos de forma otimizada.
    
    Args:
        batch_size: Número de nomes a serem gerados (padrão: 100,000)
        
    Returns:
        Lista de strings no formato "PrimeiroNome Sobrenome"
    """
    firsts = np.random.choice(FIRST_NAMES, size=batch_size)
    lasts = np.random.choice(LAST_NAMES, size=batch_size)
    return [f"{first} {last}" for first, last in zip(firsts, lasts)]

def generate_names(total: int, batch_size: int = 100_000) -> Generator[List[str], None, None]:
    """
    Gera nomes em lotes de forma otimizada.
    
    Args:
        total: Número total de nomes a serem gerados
        batch_size: Tamanho de cada lote (padrão: 100,000)
        
    Yields:
        Listas de strings contendo lotes de nomes
    """
    remaining = total
    while remaining > 0:
        current_batch = min(batch_size, remaining)
        yield generate_names_batch(current_batch)
        remaining -= current_batch

def generate_names_to_file(total: int, output_file: str, batch_size: int = 100_000) -> None:
    """
    Gera nomes e salva em um arquivo de forma otimizada.
    
    Args:
        total: Número total de nomes a serem gerados
        output_file: Caminho do arquivo de saída
        batch_size: Tamanho de cada lote (padrão: 100,000)
    """
    # Cria o diretório de saída se não existir
    output_dir = dirname(abspath(output_file))
    if output_dir and not exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
    
    # Cria o arquivo vazio
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('')  # Cria o arquivo vazio
    
    # Gera e salva em lotes
    for batch in generate_names(total, batch_size):
        with open(output_file, 'a', encoding='utf-8') as f:
            f.write('\n'.join(batch) + '\n')
