from crewai.flow.flow import Flow, start

from crew.request_routing_crew.request_routing_crew import Routing_crew

class SimpleFlow(Flow):

    @start()
    def start_flow(self):
        crew_results = Routing_crew.kickoff(inputs={
            "query": "how to get a loan"
        })
        crew_re = crew_results.model_dump()
        print('**************', (crew_re.values()))


flow = SimpleFlow()

result = flow.kickoff()

print("Flow result: ", result)