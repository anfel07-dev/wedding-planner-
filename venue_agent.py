from dotenv import load_dotenv
load_dotenv(r"C:\Users\anfal\Documents\lca-lc-foundations\.env")

from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain_tavily import TavilySearch

model = init_chat_model("groq:openai/gpt-oss-20b")

venue_agent = create_agent(
    model=model,
    tools=[TavilySearch(max_results=3)],
        system_prompt=(
        "You are a wedding venue specialist. "
        "You are given a destination, a guest count, a budget and a style. "
        "Do ONE web search for wedding venues that match, then suggest 3 venues. "
        "For each venue give the name, one line on why it fits, and an approximate price. "
        "Never ask the user follow-up questions. If something is missing, make a "
        "reasonable assumption and say what you assumed. "
        "Write plain text as a short numbered list, not a table. "
        "Never include citation markers or reference codes. Put the source website name in plain words instead. "
        "Only state prices that appear in the search results, in the currency the source used. "
        "Do not claim the options fit the budget unless a listed price is clearly below it. "
        "Keep the whole answer under 150 words."
    ),
)

if __name__ == "__main__":
    result = venue_agent.invoke({
        "messages": [{
            "role": "user",
            "content": "Destination: Santorini, Greece. Guests: 40. Budget: 30000 USD. Style: romantic, sea view.",
        }]
    })
    print(result["messages"][-1].content)