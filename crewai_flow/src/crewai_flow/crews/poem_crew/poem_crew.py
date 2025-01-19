import os

from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from pydantic import BaseModel, Field

os.environ["OPENAI_API_KEY"] = "****************************"

basic_llm = LLM(model="gpt-4o", temperature=0)

class RequestRouting(BaseModel):
    class RequestRouting(BaseModel):
        crew: str = Field(..., description="Crew must be one of the following [customer service, simple chat, complete the form]")


@CrewBase
class RoutingCrew:
    """Routing Crew"""
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def request_routing_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["request_routing_agent"],
            llm=basic_llm,
        )

    @task
    def request_routing_agent_task(self) -> Task:
        return Task(
            config=self.tasks_config["request_routing_agent_task"],
            output_pydantic=RequestRouting
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
