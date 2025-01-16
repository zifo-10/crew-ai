from crewai import Agent, Task, Crew, Process, LLM
import os

from pydantic import BaseModel, Field

os.environ["OPENAI_API_KEY"] = "sk-***************"

basic_llm = LLM(model="gpt-4o", temperature=0)


class RequestRouting(BaseModel):
    class RequestRouting(BaseModel):
        crew: str = Field(..., description="Crew must be one of the following [customer service, simple chat, complete the form]")


request_routing_agent = Agent(
    role='You have to decide where to pass this query to get the best response.',
    goal='To route the request to the best Crew for the query by selecting one of the available Crews.',
    backstory='''This Agent is the first step in the process of generating a chatbot response.
                         It receives the user query and decides which Crew to pass it to for the best response.''',
    llm=basic_llm,
    verbose=True,
)

request_routing_agent_task = Task(
    description='''
            - Our chatbot has received a This Query {query}. We need to decide which Crew to pass this query to for the best response
            - Crew must be one of the following ["customer service", "simple chat", "complete the form"]
            - each Crew has a different area of expertise and will give a different response to the same query.
            - We need to decide which Crew to pass this query to for the best response.''',
    output_pydantic=RequestRouting,
    expected_output='pydantic Model with the Crew name',
    agent=request_routing_agent
)


Routing_crew = Crew(
    agents=[
        request_routing_agent
    ],
    tasks=[
        request_routing_agent_task
    ],
    process=Process.sequential,
)
