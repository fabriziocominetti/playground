# A2A Demo with Google ADK

Mini proof-of-concept of Agent-to-Agent (A2A) communication built with Google ADK.

## What this project does

- Simulates a purchase flow between a `Buyer Agent` and a `Seller Agent`.
- The buyer sends structured intents to the seller through the A2A protocol (JSON-RPC).
- The seller responds with:
  - `message` (text for the user)
  - `structured_data` (machine-readable data, including `next_step`)
- The buyer uses `next_step` to drive a state machine until checkout is completed.

## Main files

- `seller_agent.py`: exposes the seller agent through an A2A endpoint (`to_a2a` + `uvicorn`).
- `buyer_agent.py`: interactive CLI client that talks to the remote seller and manages the workflow.
- `.env`: local configuration (API key and model).

## Prerequisites

- Python 3.11+
- Installed dependencies (`google-adk`, `python-dotenv`, `uvicorn`, etc.)
- Valid Gemini API key

## Configuration

Create or update `.env` in the project root:

```env
GOOGLE_API_KEY=your_api_key_here
GOOGLE_MODEL=gemini-2.0-flash
```

## Quick start

Open two terminals in the project folder.

Terminal 1:

```bash
python seller_agent.py
```

Terminal 2:

```bash
python buyer_agent.py
```

Then follow the console prompts to simulate the purchase flow.

## Technical notes

- The buyer uses `RemoteA2aAgent` + `Runner` with in-memory services.
- The seller enforces JSON output with mandatory `next_step`.
- The buyer includes robust fallbacks when the LLM response is not perfectly formatted.

## Quick troubleshooting

- API key error:
  - verify `GOOGLE_API_KEY` in `.env`
- Model not found error:
  - change `GOOGLE_MODEL` (for example `gemini-2.0-flash`) and restart the seller
- Port already in use:
  - free up `8080` or set `PORT` before starting the seller
