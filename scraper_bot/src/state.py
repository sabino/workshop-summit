import os
import yaml
from loguru import logger

STATE_FILE = 'data/state/state.yml'

def load_state():
    logger.debug(f"Verificando se o arquivo de estado existe: {STATE_FILE}")
    if os.path.exists(STATE_FILE):
        logger.debug(f"O arquivo de estado existe. Carregando estado de: {STATE_FILE}")
        with open(STATE_FILE, 'r') as file:
            state = yaml.safe_load(file)
            logger.debug("Estado carregado com sucesso.")
            return state
    logger.debug("O arquivo de estado não existe. Retornando estado vazio.")
    return {}

def save_state(state):
    logger.debug(f"Salvando estado no arquivo: {STATE_FILE}")
    with open(STATE_FILE, 'w') as file:
        yaml.safe_dump(state, file)
        logger.debug("Estado salvo com sucesso.")
