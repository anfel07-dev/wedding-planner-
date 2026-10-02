from typing import TypedDict


class WeddingState(TypedDict):
    origin: str
    destination: str
    departure_date: str
    return_date: str
    travelers: int

    guests: int
    budget: str
    style: str
    music_genre: str

    travel_result: str
    venue_result: str
    dj_result: str

    