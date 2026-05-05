# buyer_agent.py

import asyncio
import json
import os
from typing import Any, Optional

from google.adk.agents.remote_a2a_agent import RemoteA2aAgent
from google.adk.artifacts.in_memory_artifact_service import InMemoryArtifactService
from google.adk.runners import Runner
from google.adk.sessions.in_memory_session_service import InMemorySessionService
from google.adk.utils.context_utils import Aclosing
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

# The URL where our Seller Agent is listening
SELLER_AGENT_URL = "http://localhost:8080"
SELLER_AGENT_CARD_URL = f"{SELLER_AGENT_URL}/.well-known/agent.json"

INTENT_TO_NEXT_STEP = {
    "FIND_PRODUCTS": "AWAIT_SELECTION",
    "CONFIRM_OFFER": "AWAIT_CART_CONFIRM",
    "CONFIRM_CART": "AWAIT_PAYMENT_AUTH",
    "AUTHORIZE_PAYMENT": "COMPLETED",
}

NEXT_STEP_TO_INTENT = {
    "AWAIT_SELECTION": "CONFIRM_OFFER",
    "AWAIT_CART_CONFIRM": "CONFIRM_CART",
    "AWAIT_PAYMENT_AUTH": "AUTHORIZE_PAYMENT",
}


def extract_json_payload(raw_text: str) -> Optional[dict[str, Any]]:
    """Extracts the first valid JSON object from a string."""
    text = (raw_text or "").strip()
    if not text:
        return None

    # Direct attempt
    try:
        parsed = json.loads(text)
        if isinstance(parsed, dict):
            return parsed
    except json.JSONDecodeError:
        pass

    # Fallback: look for a parsable {...} substring
    start = text.find("{")
    while start != -1:
        end = text.rfind("}")
        while end > start:
            candidate = text[start : end + 1]
            try:
                parsed = json.loads(candidate)
                if isinstance(parsed, dict):
                    return parsed
            except json.JSONDecodeError:
                end = text.rfind("}", 0, end)
                continue
            break
        start = text.find("{", start + 1)
    return None


def normalize_seller_response(
    response: dict[str, Any], raw_response: str, current_intent: str
) -> tuple[str, dict[str, Any], str]:
    """Normalizes the seller's response to keep the state machine robust."""
    message_for_user = response.get("message")
    if not isinstance(message_for_user, str) or not message_for_user.strip():
        message_for_user = raw_response or "(No textual response from the seller)"

    structured_data = response.get("structured_data")
    if not isinstance(structured_data, dict):
        structured_data = {}

    next_step = structured_data.get("next_step")
    if not isinstance(next_step, str) or not next_step.strip():
        next_step = INTENT_TO_NEXT_STEP.get(current_intent, "AWAIT_SELECTION")
        structured_data["next_step"] = next_step

    return message_for_user, structured_data, next_step


async def send_turn(
    runner: Runner, user_id: str, session_id: str, payload: dict[str, Any]
) -> str:
    """Sends a turn to the remote Seller via ADK Runner/A2A and returns the final text."""
    content = types.Content(role="user", parts=[types.Part(text=json.dumps(payload, ensure_ascii=False))])
    final_text = ""
    async with Aclosing(
        runner.run_async(user_id=user_id, session_id=session_id, new_message=content)
    ) as agen:
        async for event in agen:
            if event.error_message:
                raise RuntimeError(f"Error from remote seller: {event.error_message}")
            if event.content and event.content.parts:
                text = "".join(part.text or "" for part in event.content.parts).strip()
                if text:
                    final_text = text
    return final_text


async def main():
    """
    Main function that simulates a purchasing session from the terminal.
    """
    print("--- Buyer Agent Initialized ---")
    print("I will simulate a conversation with a Seller Agent on your behalf.")

    if not os.environ.get("GOOGLE_API_KEY"):
        raise RuntimeError(
            "GOOGLE_API_KEY variable not set. "
            "Set it before starting the seller and buyer."
        )

    remote_seller = RemoteA2aAgent(
        name="PremiumSellerRemote",
        agent_card=SELLER_AGENT_CARD_URL,
    )
    session_service = InMemorySessionService()
    artifact_service = InMemoryArtifactService()

    runner = Runner(
        app_name="buyer_app",
        agent=remote_seller,
        session_service=session_service,
        artifact_service=artifact_service,
    )

    try:
        # Mock user data
        user_id = "demo-buyer"
        customer_id = "USR-8899"
        
        session = await session_service.create_session(app_name="buyer_app", user_id=user_id)
        
        initial_query = input("What are you looking for? (e.g., 'a laptop' or 'an OLED smartphone') > ")

        # The seller's response will always contain the expected next action
        next_step = ""

        # Let's start the conversation with the first request
        current_intent = "FIND_PRODUCTS"
        current_params = {"search_query": initial_query, "user_id": customer_id}

        # Conversation loop: continues until the seller says 'COMPLETED'
        while next_step != "COMPLETED":
            print(f"\n[Buyer] Calling the Seller Agent with intent '{current_intent}'...")
            request_payload = {
                "intent": current_intent,
                "parameters": current_params,
            }

            raw_response = await send_turn(
                runner=runner,
                user_id=user_id,
                session_id=session.id,
                payload=request_payload,
            )

            if "No API key was provided" in raw_response:
                raise RuntimeError(
                    "The Seller responded with an API key error. "
                    "Configure GOOGLE_API_KEY in the terminal."
                )
            if "models/" in raw_response and "NOT_FOUND" in raw_response:
                raise RuntimeError(
                    "The model configured in the Seller is not available for your API key. "
                    "Set GOOGLE_MODEL in the .env (e.g. gemini-2.0-flash) and restart the seller."
                )

            response = extract_json_payload(raw_response) or {"message": raw_response}

            # Extract data from the Seller's response
            message_for_user, structured_data, next_step = normalize_seller_response(
                response=response,
                raw_response=raw_response,
                current_intent=current_intent,
            )

            print("\n-------------------------------------------")
            print(f"[Seller] Message for you: {message_for_user}")
            print(f"[Buyer] Structured data received: {structured_data}")
            print("-------------------------------------------")

            if next_step == "COMPLETED":
                print("\n[OK] Purchasing session completed!")
                break

            # Ask the user for input for the next step
            user_input = input("Reply to the seller (or press Enter to confirm): ")

            # Simple logic to map user input to the next intent
            if next_step in NEXT_STEP_TO_INTENT:
                current_intent = NEXT_STEP_TO_INTENT[next_step]
            elif next_step != "COMPLETED":
                raise RuntimeError(
                    f"next_step not recognized by the Seller: {next_step}"
                )
            
            current_params = {"user_input": user_input}

    finally:
        await runner.close()

if __name__ == "__main__":
    asyncio.run(main())
