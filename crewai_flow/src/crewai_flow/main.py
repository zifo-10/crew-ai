#!/usr/bin/env python
import json

from crewai.flow.flow import Flow, start
from pydantic import BaseModel

from crewai_flow.src.crewai_flow.crews.form_filler.form_filler_crew import FormFillerCrew
from crewai_flow.src.crewai_flow.crews.orchestrator.orchestrator_crew import OrchestratorCrew
from crewai_flow.src.crewai_flow.crews.simple_rag.simple_rag_crew import SimpleRagCrew


class ExampleState(BaseModel):
    form_filler: bool = False


class RagFlow(Flow[ExampleState]):

    @start()
    def orchestrator(self):
        """
        Main entry point: Determines whether to continue form filling or process a new request.
        """
        if self.state.form_filler:
            print("[INFO] Continuing form filling process...")
            return self.continue_form_filling()

        inputs = {
            "query": "i want to schedule a meeting",
            "list_messages": ["when i can see you", "i want to meet you", "can we meet today"]
        }

        print("[INFO] Sending request to OrchestratorCrew...")
        orchestrator_result = OrchestratorCrew().crew().kickoff(inputs=inputs)
        result_dict = json.loads(orchestrator_result.raw)

        next_crew = result_dict.get("next_crew")

        if next_crew == "form filler":
            self.state.form_filler = True
            return self.continue_form_filling(
            )

        elif next_crew == "simple chat":
            return self.process_simple_chat(
                translated_query=result_dict.get("processed_query", {}).get("translated_query", ""),
                similar_queries=result_dict.get("processed_query", {}).get("similar_queries", [])
            )

        print("[WARNING] No valid crew identified. Defaulting to simple chat.")
        return self.process_simple_chat(translated_query=inputs["query"], similar_queries=[])

    def continue_form_filling(self):
        """
        Handles the form-filling process until completion.
        """
        print("[INFO] Starting form-filling process...")
        form_filler_result = FormFillerCrew().crew().kickoff()
        # Check if the result is already a dictionary
        form_filler_dict = json.loads(form_filler_result.raw)

        # Process the form filling result
        if form_filler_dict.get("form_filled"):
            print("[SUCCESS] Form completed. Proceeding to email sending...")
            self.state.form_filler = False
            return self.send_email()

        next_question = form_filler_dict.get("next_question")

        if next_question:
            print(f"[INFO] Asking next question: {next_question}")
        else:
            print("[ERROR] No next question found in the response.")
            return {"error": "No next question found in the response."}

        return next_question

    def process_simple_chat(self, translated_query, similar_queries):
        """
        Handles simple RAG-based responses.
        """
        print("[INFO] Processing Simple Chat using RAG...")
        return SimpleRagCrew().crew().kickoff(inputs={"query": translated_query, "list_messages": similar_queries})

    def send_email(self):
        """
        Handles email sending after form completion.
        """
        print("[INFO] Sending email with completed form...")
        return {"message": "Email Sent Successfully!"}


def kickoff():
    print("[INFO] Kicking off the RagFlow process...")
    flow = RagFlow()
    flow.kickoff()


if __name__ == "__main__":
    kickoff()
