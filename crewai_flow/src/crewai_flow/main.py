#!/usr/bin/env python

from crewai.flow.flow import Flow, start

from crewai_flow.src.crewai_flow.crews.poem_crew.poem_crew import RoutingCrew


class PoemFlow(Flow):

    @start()
    def generate_sentence_count(self):
        print("Routing Crew - will start")
        result = (
            RoutingCrew()
            .crew()
            .kickoff(inputs={
                "query": "how to get a loan"
            })
        )
        print("Routing Crew Result: ", result.raw)


def kickoff():
    poem_flow = PoemFlow()
    poem_flow.kickoff()


def plot():
    poem_flow = PoemFlow()
    poem_flow.plot()


if __name__ == "__main__":
    kickoff()
