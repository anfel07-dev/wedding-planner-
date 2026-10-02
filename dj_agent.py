import sqlite3
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(r"C:\Users\anfal\Documents\lca-lc-foundations\.env")

from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain.tools import tool

DB = Path(__file__).parent / "Chinook.db"

@tool
def run_sql(query: str) -> str:
    """Run a read-only SQL SELECT query on the music database and return the rows."""
    if not query.strip().lower().startswith("select"):
        return "Error: only SELECT queries are allowed."
    try:
        con = sqlite3.connect(f"file:{DB.as_posix()}?mode=ro", uri=True)
        rows = con.execute(query).fetchall()
        con.close()
        return str(rows[:30]) if rows else "No rows found."
    except Exception as e:
        return f"SQL error: {e}"

model = init_chat_model("groq:openai/gpt-oss-20b")

dj_agent = create_agent(
    model=model,
    tools=[run_sql],
    system_prompt=(
        "You are a wedding DJ. You are given a music genre or vibe. "
        "Use the run_sql tool to build a playlist from the music database. "
        "Tables: Genre(GenreId, Name), Track(TrackId, Name, AlbumId, GenreId, Milliseconds), "
        "Album(AlbumId, Title, ArtistId), Artist(ArtistId, Name). "
        "First look up the genre names with: SELECT Name FROM Genre. "
        "Then pick the closest genre and query 10 tracks with their artist names, "
        "joining Track, Album, Artist and Genre. "
        "Never ask follow-up questions. If the genre does not exist, pick the closest one "
        "and say which you picked. "
        "Answer as a plain numbered list: Song - Artist. No tables."
    ),
)

if __name__ == "__main__":
    result = dj_agent.invoke({
        "messages": [{"role": "user", "content": "Genre: Jazz. Vibe: romantic dinner and slow dance."}]
    })
    print(result["messages"][-1].content)