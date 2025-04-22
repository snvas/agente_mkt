from langchain_community.tools import DuckDuckGoSearchRun
from crewai.tools import BaseTool
from typing import Any
import datetime
from pydantic import BaseModel, Field

class WebSearchSchema(BaseModel):
    query: str = Field(description="O texto que você quer pesquisar na web")

class ContentResearchSchema(BaseModel):
    query: str = Field(description="O tópico ou assunto que você quer pesquisar em detalhes")

class TrendAnalysisSchema(BaseModel):
    topic: str = Field(description="O tópico para analisar tendências atuais")

class WebSearchTool(BaseTool):
    name: str = "Web Search"
    description: str = "Ferramenta para pesquisar informações na web sobre qualquer tópico."
    args_schema: type[BaseModel] = WebSearchSchema

    def _run(self, query: str) -> str:
        search = DuckDuckGoSearchRun()
        results = search.run(query)
        return results

class ContentResearchTool(BaseTool):
    name: str = "Content Research"
    description: str = "Pesquisa informações detalhadas sobre um tópico específico para criação de conteúdo."
    args_schema: type[BaseModel] = ContentResearchSchema

    def _run(self, query: str) -> str:
        search = DuckDuckGoSearchRun()
        results = search.run(query)
        return results

class TrendAnalysisTool(BaseTool):
    name: str = "Trend Analysis"
    description: str = "Analisa tendências atuais relacionadas ao tópico para criar conteúdo relevante."
    args_schema: type[BaseModel] = TrendAnalysisSchema

    def _run(self, topic: str) -> str:
        search = DuckDuckGoSearchRun()
        query = f"latest trends {topic} {datetime.datetime.now().year}"
        results = search.run(query)
        return results

# Initialize tools
web_search = WebSearchTool()
content_research = ContentResearchTool()
trend_analysis = TrendAnalysisTool()