import os
from typing import Optional, Dict

from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from pydantic import BaseModel, Field

# Load API key securely (Avoid hardcoding in production)
os.environ["OPENAI_API_KEY"] = "****************************"

# Initialize LLM with optimal parameters
basic_llm = LLM(model="gpt-4o", temperature=0)

class FormFillerAnswer(BaseModel):
    """Response model for form-filling completion status."""
    next_question: Optional[str] = Field(None, title="Next question if the form is not fully completed")
    form_filled: Optional[bool] = Field(None, title="Indicates whether the form is fully filled")

@CrewBase
class FormFillerCrew:
    """Handles form completion based on user conversation."""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def form_filler_agent(self) -> Agent:
        """Agent responsible for guiding the user through the form completion process."""
        return Agent(
            config=self.agents_config["form_filler_agent"],
            llm=basic_llm,
        )

    @task
    def form_filler_task(self) -> Task:
        """Task that processes the form-filling conversation and determines completion status."""
        return Task(
            config=self.tasks_config["form_filler_task"],
            output_pydantic=FormFillerAnswer
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Form Filler Crew."""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )
