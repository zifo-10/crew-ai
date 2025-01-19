import os

from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from pydantic import BaseModel, Field

os.environ["OPENAI_API_KEY"] = "***********************"

basic_llm = LLM(model="gpt-4o", temperature=0)

class SimpleChatAnswer(BaseModel):
    answer: str = Field(..., description="Answer to the query")


@CrewBase
class SimpleRagCrew:
    """Routing Crew"""
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def simple_rag_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["simple_rag_agent"],
            llm=basic_llm,
        )

    @task
    def simple_rag_task(self) -> Task:
        return Task(
            config=self.tasks_config["simple_rag_task"],
            output_pydantic=SimpleChatAnswer
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Research Crew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )
