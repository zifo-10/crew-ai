#!/usr/bin/env python
import json

from crewai.flow.flow import Flow, start, router, listen
from pydantic import BaseModel, Field

from crewai_flow.src.crewai_flow.crews.request_router.request_router_crew import RoutingCrew
from crewai_flow.src.crewai_flow.crews.simple_rag.simple_rag_crew import SimpleRagCrew


class ExampleState(BaseModel):
    crew: str = ""

class RagFlow(Flow[ExampleState]):

    @start()
    def request_router(self):
        result = (
            RoutingCrew()
            .crew()
            .kickoff(inputs={
                "query": "how to be in this competition?"
            })
        )
        result_dict = json.loads(result.raw)
        if  str(result_dict["crew"]) == 'customer service':
            self.state.crew = 'customer service'
        elif str(result_dict["crew"]) == 'complete the form':
            self.state.crew = "complete the form"
        else:
            self.state.crew = "simple chat"

    @router(request_router)
    def second_method(self):
        return self.state.crew

    @listen("customer service")
    def third_method(self):
        print("Customer service running")

    @listen("complete the form")
    def fourth_method(self):
        print("Complete the form running")

    @listen("simple chat")
    def fifth_method(self):
        result = (
            SimpleRagCrew()
            .crew()
            .kickoff(inputs={
                "query": "How are you?"
            })
        )
        print('result', result.raw)

def kickoff():
    poem_flow = RagFlow()
    poem_flow.kickoff()

kickoff()
