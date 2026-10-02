import asyncio, json
from langchain_mcp_adapters.client import MultiServerMCPClient

async def main():
    client = MultiServerMCPClient({
        "travel_server": {"transport": "streamable_http", "url": "https://mcp.kiwi.com"}
    })
    tools = await client.get_tools()
    t = [x for x in tools if x.name == "search-flight"][0]
    print("Description length (characters):", len(t.description))
    schema = t.args_schema if isinstance(t.args_schema, dict) else t.args_schema.model_json_schema()
    print("Required fields:", schema.get("required"))
    for name, spec in schema.get("properties", {}).items():
        print("-", name, "|", spec.get("type"), "|", (spec.get("description") or "")[:80].replace("\n", " "))

asyncio.run(main())