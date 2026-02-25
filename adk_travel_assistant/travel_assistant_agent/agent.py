from google.adk.agents import LlmAgent
from google.adk.tools.agent_tool import AgentTool

import os
from dotenv import load_dotenv

from . import prompt
from .subagents.research.agent import travel_researcher_agent
from .subagents.planner.agent import itinerary_planner_agent
from .subagents.image_generation.agent import image_generator_agent

load_dotenv()


root_agent = LlmAgent(
    name="travel_assistant_coordinator",
    model="gemini-2.5-flash",
    description="Master Agent",
    instruction=prompt.TRAVEL_ASSISTANT_COORDINATOR_PROMPT,
    tools=[
        AgentTool(agent=travel_researcher_agent),
        AgentTool(agent=itinerary_planner_agent),
        AgentTool(agent=image_generator_agent),
    ]
)
