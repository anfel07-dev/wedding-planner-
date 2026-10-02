import asyncio
from dotenv import load_dotenv
load_dotenv(r"C:\Users\anfal\Documents\lca-lc-foundations\.env")

from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_mcp_adapters.client import MultiServerMCPClient

model = init_chat_model("groq:openai/gpt-oss-20b")

SYSTEM_PROMPT = (
    "You are a wedding travel agent. You are given an origin city, a destination, "
    "travel dates and a number of travelers. "
    "Use the search_flights tool ONCE to find round-trip flights. "
    "Use airport codes (for example Paris = CDG, Santorini = JTR) and dates as dd/mm/yyyy. "
    "Suggest the best 2 or 3 options with price, airline, duration and a booking link if available. "
    "Never ask follow-up questions. If something is missing, make a reasonable "
    "assumption and say what you assumed. "
    "Write plain text as a short numbered list, not a table. "
    "Keep the whole answer under 150 words."
)

MAX_CHARS = 4000  # cut flight results so the model never reads too much

async def build_travel_agent():
    client = MultiServerMCPClient({
        "travel_server": {
            "transport": "streamable_http",
            "url": "https://mcp.kiwi.com",
        }
    })
    all_tools = await client.get_tools()
    kiwi = [t for t in all_tools if t.name == "search-flight"][0]

    @tool
    async def search_flights(fly_from: str, fly_to: str, departure_date: str,
                             return_date: str, adults: int = 1) -> str:
        """Search round-trip flights. Use airport codes like CDG or JTR and dates as dd/mm/yyyy."""
        raw = await kiwi.ainvoke({
            "flyFrom": fly_from,
            "flyTo": fly_to,
            "departureDate": departure_date,
            "returnDate": return_date,
            "adults": adults,
            "currency": "EUR",
            "locale": "en",
        })
        return str(raw)[:MAX_CHARS]

    return create_agent(model=model, tools=[search_flights], system_prompt=SYSTEM_PROMPT)

async def main():
    agent = await build_travel_agent()
    result = await agent.ainvoke({
        "messages": [{
            "role": "user",
            "content": "Origin: Paris. Destination: Santorini, Greece. Depart: 10/06/2027. Return: 17/06/2027. Travelers: 2.",
        }]
    })
    print(result["messages"][-1].content)

if __name__ == "__main__":
    asyncio.run(main())

    