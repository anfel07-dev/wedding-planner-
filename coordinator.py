import asyncio

from wedding_state import WeddingState
from dj_agent import dj_agent
from venue_agent import venue_agent
from travel_agent import build_travel_agent


async def coordinator(state: WeddingState) -> WeddingState:
    print("\n🎯 COORDINATOR")
    print("Understanding the wedding plan...\n")

    # --------------------------------------------------
    # 1. DJ AGENT
    # --------------------------------------------------

    print("🎵 Calling DJ agent...")

    dj_result = dj_agent.invoke({
        "messages": [{
            "role": "user",
            "content": (
                f"Genre: {state['music_genre']}. "
                f"Vibe: {state['style']}."
            )
        }]
    })

    state["dj_result"] = dj_result["messages"][-1].content

    print("✅ DJ agent finished.")

    # --------------------------------------------------
    # 2. VENUE AGENT
    # --------------------------------------------------

    print("\n🏛️ Calling venue agent...")

    venue_result = venue_agent.invoke({
        "messages": [{
            "role": "user",
            "content": (
                f"Destination: {state['destination']}. "
                f"Guests: {state['guests']}. "
                f"Budget: {state['budget']}. "
                f"Style: {state['style']}."
            )
        }]
    })

    state["venue_result"] = venue_result["messages"][-1].content

    print("✅ Venue agent finished.")

    # --------------------------------------------------
    # 3. TRAVEL AGENT
    # --------------------------------------------------

    print("\n✈️ Calling travel agent...")

    travel_agent = await build_travel_agent()

    travel_result = await travel_agent.ainvoke({
        "messages": [{
            "role": "user",
            "content": (
                f"Origin: {state['origin']}. "
                f"Destination: {state['destination']}. "
                f"Depart: {state['departure_date']}. "
                f"Return: {state['return_date']}. "
                f"Travelers: {state['travelers']}."
            )
        }]
    })

    state["travel_result"] = travel_result["messages"][-1].content

    print("✅ Travel agent finished.")

    return state


async def main():

    wedding = WeddingState(
        origin="Paris",
        destination="Santorini, Greece",
        departure_date="10/06/2027",
        return_date="17/06/2027",
        travelers=2,

        guests=40,
        budget="30000 USD",
        style="romantic, sea view",
        music_genre="Jazz",

        travel_result="",
        venue_result="",
        dj_result="",
    )

    result = await coordinator(wedding)

    # --------------------------------------------------
    # FINAL WEDDING PLAN
    # --------------------------------------------------

    print("\n")
    print("=" * 60)
    print("💍 FINAL WEDDING PLAN")
    print("=" * 60)

    print("\n✈️ FLIGHTS")
    print(result["travel_result"])

    print("\n🏛️ VENUES")
    print(result["venue_result"])

    print("\n🎵 MUSIC")
    print(result["dj_result"])

    print("\n" + "=" * 60)


if __name__ == "__main__":
    asyncio.run(main())