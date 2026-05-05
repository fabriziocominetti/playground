# seller_agent.py

import os
import json
from google.adk.agents.llm_agent import Agent
from google.adk.tools.function_tool import FunctionTool
from google.adk.a2a.utils.agent_to_a2a import to_a2a
import uvicorn
from dotenv import load_dotenv

load_dotenv()

# --- 1. TOOLSET (MOCK OF EXTERNAL SERVICES) ---

@FunctionTool
def get_customer_data(user_id: str) -> str:
    """Retrieves customer info (via customer_data.json): discounts, address, and payment method."""
    print(f"TOOL CALLED: get_customer_data for user_id: {user_id}")
    try:
        with open('customer_data.json', 'r') as file:
            data = json.load(file)
            customers = data.get("customers", [])
            
            # Find the specific user
            for customer in customers:
                if customer.get("user_id") == user_id:
                    return json.dumps(customer)
            
            # If loop finishes without returning, user was not found
            return json.dumps({"error": "User not found"})
            
    except FileNotFoundError:
        return json.dumps({"error": "Customer data file 'customer_data.json' not found."})
    except json.JSONDecodeError:
        return json.dumps({"error": "Error decoding 'customer_data.json'."})

@FunctionTool
def get_catalog_products(search_query: str) -> str:
    """Searches for products in the catalog and returns their details and price."""
    print(f"TOOL CALLED: get_catalog_products for query: {search_query}")
    try:
        with open('products_catalog.json', 'r') as file:
            catalog_data = json.load(file)
            products = catalog_data.get("products", [])
            
            # Filter products based on the search query (checking name and description)
            query = search_query.lower()
            filtered_products = [
                p for p in products 
                if query in p.get("name", "").lower() or query in p.get("description", "").lower()
            ]
            
            # If no specific match is found, return the full list so the LLM can decide
            return json.dumps(filtered_products if filtered_products else products)
            
    except FileNotFoundError:
        return json.dumps({"error": "Catalog file 'products_catalog.json' not found."})
    except json.JSONDecodeError:
        return json.dumps({"error": "Error decoding 'products_catalog.json'."})

@FunctionTool
def finalize_order_and_send_email(user_email: str, order_summary: str) -> str:
    """Sends order confirmation and closes the transaction."""
    print(f"TOOL CALLED: finalize_order_and_send_email to {user_email}")
    return json.dumps({"status": "success", "order_id": "A2A-REDIS-999"})

# --- 2. AGENT DEFINITION ---

CUSTOM_SELLER_PROMPT = """
You are a Premium Seller Agent who sells electronics products.

Your goal is to guide the user through a well-defined sales workflow:

1. **Offer**: When the user asks for a product, use the tools to find the product and user data. Present a personalized offer with a discount, if applicable. Your state must become 'AWAIT_SELECTION'.
2. **Cart Confirmation**: If the user accepts, retrieve the address from memory and ask for confirmation. Your state must become 'AWAIT_CART_CONFIRM'.
3. **Payment Confirmation**: If the user confirms the address, retrieve the payment method from memory and ask for authorization to charge. Your state must become 'AWAIT_PAYMENT_AUTH'.
4. **Order Closure**: If the user authorizes, execute the tool to finalize the order and send the email. Communicate the success and the order ID. Your state must become 'COMPLETED'.

Use memory to maintain the state of the conversation between messages.
The checkout link is always: https://shop.test-vendor.com/checkout

The user's input arrives as a textual JSON with the format:
{"intent":"<INTENT>", "parameters":{...}}

ALWAYS respond with valid JSON (no markdown/backticks/extra text) in the format:
{
  "message": "text for the user",
  "structured_data": {
    "next_step": "AWAIT_SELECTION|AWAIT_CART_CONFIRM|AWAIT_PAYMENT_AUTH|COMPLETED",
    "offer_id": "optional",
    "price": "optional",
    "checkout_url": "optional"
  }
}

Mandatory rules:
- Never respond in natural language outside the JSON.
- `structured_data.next_step` must ALWAYS be present and populated.
- Map intent -> next_step:
  - FIND_PRODUCTS -> AWAIT_SELECTION
  - CONFIRM_OFFER -> AWAIT_CART_CONFIRM
  - CONFIRM_CART -> AWAIT_PAYMENT_AUTH
  - AUTHORIZE_PAYMENT -> COMPLETED
"""

PORT = int(os.environ.get("PORT", 8080))
MODEL_NAME = os.environ.get("GOOGLE_MODEL", "gemini-2.0-flash")

smart_seller_agent = Agent(
    model=MODEL_NAME,
    name='PremiumSellerAgent',
    instruction=CUSTOM_SELLER_PROMPT,
    tools=[get_customer_data, get_catalog_products, finalize_order_and_send_email]
)

# --- 3. A2A EXPOSURE AND STARTUP ---

seller_a2a_endpoint = to_a2a(
    smart_seller_agent,
    host="localhost",
    port=PORT,
    protocol="http",
)

if __name__ == "__main__":
    if not os.environ.get("GOOGLE_API_KEY"):
        raise RuntimeError(
            "GOOGLE_API_KEY variable not set. "
            "Set it in the terminal before starting the seller."
        )
    print(f"INFO:     Seller Agent starting up.")
    print(f"INFO:     Model: {MODEL_NAME}")
    print("INFO:     Memory backend: InMemoryMemoryService (local test mode)")
    print(f"INFO:     Listening on http://0.0.0.0:{PORT}")
    uvicorn.run(seller_a2a_endpoint, host="0.0.0.0", port=PORT)
