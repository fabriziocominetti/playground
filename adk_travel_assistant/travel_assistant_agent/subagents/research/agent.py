from google.adk.agents import LlmAgent
from google.adk.tools import google_search


travel_researcher_agent = LlmAgent(
    name="travel_researcher",
    model="gemini-2.5-flash",
    instruction="""
                Find real-time travel info: flight estimates, hotel availability, and local events for the user's destination.
                """,
    tools=[
        google_search
    ]
)
