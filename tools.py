from langchain_community.tools import DuckDuckGoSearchRun
from crewai.tools import BaseTool
import datetime
from typing import Any
from pydantic import BaseModel, Field, AliasChoices

# Initialize the DuckDuckGo search
search_tool = DuckDuckGoSearchRun()

class WebSearchSchema(BaseModel):
    query: str = Field(description="O texto que você quer pesquisar na web", validation_alias=AliasChoices("query", "description"))

class ContentResearchSchema(BaseModel):
    query: str = Field(description="O tópico ou assunto que você quer pesquisar em detalhes", validation_alias=AliasChoices("query", "description"))

class TrendAnalysisSchema(BaseModel):
    topic: str = Field(description="O tópico para analisar tendências atuais", validation_alias=AliasChoices("topic", "description"))

class WebSearchTool(BaseTool):
    name: str = "Web Search"
    description: str = "Ferramenta para pesquisar informações na web sobre qualquer tópico."
    args_schema: type[BaseModel] = WebSearchSchema

    def _run(self, query: str) -> str:
        if isinstance(query, dict):
            query = query.get('query', '')
        return search_tool.run(query)

    def _arun(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError("WebSearchTool does not support async")

class ContentResearchTool(BaseTool):
    name: str = "Content Research"
    description: str = "Pesquisa informações detalhadas sobre um tópico específico para criação de conteúdo."
    args_schema: type[BaseModel] = ContentResearchSchema

    def _run(self, query: str) -> str:
        if isinstance(query, dict):
            query = query.get('query', '')
        return search_tool.run(query)

    def _arun(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError("ContentResearchTool does not support async")

class TrendAnalysisTool(BaseTool):
    name: str = "Trend Analysis"
    description: str = "Analisa tendências atuais relacionadas ao tópico para criar conteúdo relevante."
    args_schema: type[BaseModel] = TrendAnalysisSchema

    def _run(self, topic: str) -> str:
        if isinstance(topic, dict):
            topic = topic.get('topic', '')
        query = f"latest trends {topic} {datetime.datetime.now().year}"
        return search_tool.run(query)

    def _arun(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError("TrendAnalysisTool does not support async")

# Initialize tools

web_search = WebSearchTool()
content_research = ContentResearchTool()
trend_analysis = TrendAnalysisTool()