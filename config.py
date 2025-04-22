import yaml
import os

def load_config():
    """
    Carrega as configurações dos arquivos YAML.
    
    Returns:
        dict: Dicionário com todas as configurações carregadas.
    """
    config = {}
    
    # Carrega as configurações dos agentes
    with open('config/agents.yaml', 'r') as file:
        config['agents'] = yaml.safe_load(file)
    
    # Carrega as configurações das tarefas
    with open('config/tasks.yaml', 'r') as file:
        config['tasks'] = yaml.safe_load(file)
    
    return config