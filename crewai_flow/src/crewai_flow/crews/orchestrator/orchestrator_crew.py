import os
from typing import Optional

from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from pydantic import BaseModel, Field

os.environ["OPENAI_API_KEY"] = "****************************"

basic_llm = LLM(model="gpt-4o", temperature=0)


class ProcessingAgentResponse(BaseModel):
    original_query_language: str = Field(..., description="Original query language")
    translated_query: str = Field(..., description="Translated query to be used by the next crew")
    similar_queries: list[str] = Field(..., description="List of similar queries")


class OrchestratorAgentResponse(BaseModel):
    next_crew: str = Field(..., description="Crew must be one of the following: [form filler, simple chat]")
    form_type: Optional[str] = Field(None, description="Form type to be completed")
    processed_query: ProcessingAgentResponse = Field(..., description="Processed query to be used by the next crew")


@CrewBase
class OrchestratorCrew:
    """Orchestrator Crew"""
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def processing_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["processing_agent"],
            llm=basic_llm,
        )

    @agent
    def orchestrator_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["orchestrator_agent"],
            llm=basic_llm,
        )

    @task
    def processing_task(self) -> Task:
        return Task(
            config=self.tasks_config["processing_task"],
            output_pydantic=ProcessingAgentResponse
        )

    @task
    def orchestrator_task(self) -> Task:
        return Task(
            config=self.tasks_config["orchestrator_task"],
            output_pydantic=OrchestratorAgentResponse
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Orchestrator Crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
