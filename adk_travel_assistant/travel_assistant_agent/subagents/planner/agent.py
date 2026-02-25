import os
import time
from google.adk.agents import LlmAgent


async def save_itinerary(plan_content: str):
    """Saves the final trip itinerary to a markdown file in the outputs folder."""
    output_dir = os.path.join(os.getcwd(), "travel_assistant_agent/outputs")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    ts = int(round(time.time(), 0))
    filename = f"itinerary_{ts}.md"
    filepath = os.path.join(output_dir, filename)
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(plan_content)
        
    return {"status": "success", "detail": f"Itinerary saved to {filename}", "filepath": filepath}


itinerary_planner_agent = LlmAgent(
    name="itinerary_planner",
    model="gemini-2.5-flash",
    instruction="""
                You are a travel planning expert. Your job is to create a cohesive, logic-based travel plan using the provided research.
                Focus on logistics, timing, and making the trip flow naturally.
                
                **Tool Usage:**
                - Once you have finalized the itinerary, you MUST use the `save_itinerary` tool to save it to the outputs folder.
                """,
    tools=[save_itinerary]
)
