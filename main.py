import pysqlite3
import sys
sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")

from crew import ContentCrew
from config import load_config
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class ContentResult:
    success: bool
    error_message: Optional[str] = None
    tasks_output: Optional[List] = None

def run_content_creation(topic: str, inputs: dict = None):
    """
    Executa o processo de criação de conteúdo usando a equipe de agentes.
    
    Args:
        topic (str): O tópico principal para criação de conteúdo.
        inputs (dict, optional): Informações adicionais para personalização do conteúdo. Defaults to None.
    
    Returns:
        ContentResult: Objeto contendo o resultado do processo ou mensagem de erro.
    """
    try:
        crew_instance = ContentCrew()
        
        if inputs is None:
            inputs = {}
            
        # Adiciona o tópico aos inputs para uso em todas as tarefas
        full_inputs = {
            "topic": topic,
            "target_audience": inputs.get("target_audience", ""),
            "content_goals": inputs.get("content_goals", []),
            "platforms": inputs.get("platforms", []),
            "tone": inputs.get("tone", "Profissional"),
            "additional_instructions": inputs.get("additional_instructions", "")
        }

        result = crew_instance.crew(topic=topic).kickoff(inputs=full_inputs)
        return ContentResult(success=True, tasks_output=result.tasks_output)
    except Exception as e:
        return ContentResult(success=False, error_message=f"Erro ao processar a solicitação: {str(e)}")
