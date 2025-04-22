from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from langchain_openai import ChatOpenAI
from tools import web_search, content_research, trend_analysis
from config import load_config
import datetime

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.7,
    max_tokens=4000,
    streaming=True
)

@CrewBase
class ContentCrew:
    config = load_config()

    @agent
    def content_researcher(self) -> Agent:
        return Agent(
            config=self.config['agents']['content_researcher'],
            verbose=True,
            tools=[web_search, content_research, trend_analysis],
            llm=llm,
        )

    @agent
    def content_writer(self) -> Agent:
        return Agent(
            config=self.config['agents']['content_writer'],
            verbose=True,
            tools=[web_search, content_research],
            llm=llm,
        )

    @agent
    def visual_content_creator(self) -> Agent:
        return Agent(
            config=self.config['agents']['visual_content_creator'],
            verbose=True,
            tools=[web_search],
            llm=llm,
        )

    @agent
    def social_media_strategist(self) -> Agent:
        return Agent(
            config=self.config['agents']['social_media_strategist'],
            verbose=True,
            tools=[web_search, trend_analysis],
            llm=llm,
        )

    @agent
    def content_editor(self) -> Agent:
        return Agent(
            config=self.config['agents']['content_editor'],
            verbose=True,
            tools=[web_search],
            llm=llm,
        )

    def _create_task(self, task_name: str, agent_method, topic: str) -> Task:
        """Helper method to create tasks with proper topic formatting"""
        task_config = self.config['tasks'][task_name]
        current_year = datetime.datetime.now().year
        description = task_config["description"].format(
            topic=topic,
            current_year=current_year
        )
        return Task(
            description=description,
            expected_output=task_config["expected_output"],
            agent=agent_method()
        )

    def content_research_task(self, topic: str) -> Task:
        return self._create_task("content_research_task", self.content_researcher, topic)

    def blog_post_creation_task(self, topic: str) -> Task:
        return self._create_task("blog_post_creation_task", self.content_writer, topic)

    def visual_content_task(self, topic: str) -> Task:
        return self._create_task("visual_content_task", self.visual_content_creator, topic)

    def social_media_content_task(self, topic: str) -> Task:
        return self._create_task("social_media_content_task", self.social_media_strategist, topic)

    def content_review_task(self, topic: str) -> Task:
        return self._create_task("content_review_task", self.content_editor, topic)

    def crew(self, topic: str) -> Crew:
        """Creates the Content Creation Crew"""
        return Crew(
            agents=[
                self.content_researcher(),
                self.content_writer(),
                self.visual_content_creator(),
                self.social_media_strategist(),
                self.content_editor()
            ],
            tasks=[
                self.content_research_task(topic),
                self.blog_post_creation_task(topic),
                self.visual_content_task(topic),
                self.social_media_content_task(topic),
                self.content_review_task(topic)
            ],
            process=Process.sequential,
            verbose=True,
        )