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
from typing import Dict, List, Optional, Tuple, Union, TypeVar, Generator, Any
import functools

__version__ = '1.1.0'
__author__ = 'Near Skys'
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
    """Retorna um primeiro nome aleatório.
    
    Args:
        gender: 'male', 'female' ou None para aleatório
        
    Returns:
        str: Primeiro nome capitalizado
    """
    if not FIRST_NAMES:
        _load_all_names()
    return random.choice(FIRST_NAMES)

def get_last_name() -> str:
    """Retorna um sobrenome aleatório.
    
    Returns:
        str: Sobrenome capitalizado
    """
    if not LAST_NAMES:
        _load_all_names()
    return random.choice(LAST_NAMES)

def get_full_name(gender: Optional[str] = None) -> str:
    """Retorna um nome completo aleatório.
    
    Args:
        gender: 'male', 'female' ou None para aleatório
        
    Returns:
        str: Nome completo no formato "PrimeiroNome Sobrenome"
    """
    if not FIRST_NAMES or not LAST_NAMES:
        _load_all_names()
    return f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"

# Variáveis globais para armazenar os nomes em memória
FIRST_NAMES = []
LAST_NAMES = []
_LOADED = False
_LOCK = threading.RLock()

def _load_all_names() -> None:
    """Carrega todos os nomes em memória para acesso rápido."""
    global FIRST_NAMES, LAST_NAMES, _LOADED
    
    # Usa double-checked locking para thread safety
    if _LOADED:
        return
        
    with _LOCK:
        if _LOADED:  # Verifica novamente dentro do lock
            return
            
        try:
            # Carrega nomes masculinos
            with open(FILES['first:male'], 'r', encoding='utf-8') as f:
                male_names = [line.split()[0].capitalize() for line in f]
            
            # Carrega nomes femininos
            with open(FILES['first:female'], 'r', encoding='utf-8') as f:
                female_names = [line.split()[0].capitalize() for line in f]
            
            # Carrega sobrenomes
            with open(FILES['last'], 'r', encoding='utf-8') as f:
                LAST_NAMES[:] = [line.split()[0].capitalize() for line in f]
            
            # Combina nomes masculinos e femininos
            FIRST_NAMES[:] = male_names + female_names
            _LOADED = True
            
        except Exception as e:
            raise RuntimeError(f"Falha ao carregar os arquivos de nomes: {str(e)}")

# Tenta carregar os nomes na importação, mas não falha se não conseguir
try:
    _load_all_names()
except Exception:
    pass

def generate_names_batch(batch_size: int = 100_000) -> List[str]:
    """
    Gera um lote de nomes completos de forma otimizada.
    
    Args:
        batch_size: Número de nomes a serem gerados (padrão: 100,000)
        
    Returns:
        Lista de strings no formato "PrimeiroNome Sobrenome"
    """
    if not _LOADED:
        _load_all_names()
        
    # Usa numpy para geração vetorizada
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

def generate_names_to_file(total: int, output_file: str, batch_size: int = 1_000_000) -> None:
    """
    Gera nomes e salva em um arquivo de forma otimizada.
    
    Args:
        total: Número total de nomes a serem gerados
        output_file: Caminho do arquivo de saída
        batch_size: Tamanho de cada lote (padrão: 1,000,000)
    """
    if not _LOADED:
        _load_all_names()
        
    # Cria o diretório de saída se não existir
    output_dir = dirname(abspath(output_file))
    if output_dir and not exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
    
    # Usa buffer grande para escrita em arquivo
    buffer_size = 16 * 1024 * 1024  # 16MB buffer
    
    with open(output_file, 'w', encoding='utf-8', buffering=buffer_size) as f:
        remaining = total
        while remaining > 0:
            current_batch = min(batch_size, remaining)
            names = generate_names_batch(current_batch)
            f.write('\n'.join(names) + '\n')
            remaining -= current_batch
    
    # Gera e salva em lotes
    for batch in generate_names(total, batch_size):
        with open(output_file, 'a', encoding='utf-8') as f:
            f.write('\n'.join(batch) + '\n')
