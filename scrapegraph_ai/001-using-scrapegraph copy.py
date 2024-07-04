from scrapegraphai.graphs import SmartScraperGraph, ScriptCreatorGraph
from pydantic import BaseModel, Field
from os import environ


class Event(BaseModel):
    title: str
    date: str
    description: str
    place: str
    address: str
    tags: list[str]


class EventList(BaseModel):
    events: list[Event] = Field(..., description="List of events in Joinville")


graph_config = {
    "llm": {
        "api_key": environ["OPENAI_API_KEY"],
        "model": "gpt-4o",
        "temperature": 0,
    },
    "library": "playwright",
    "headless": False,
    "verbose": True,
    "burr_kwargs": {
        "project_name": "test-scraper",
        "app_instance_id": "some_id",
    },
}

script_creator_graph = SmartScraperGraph(
    prompt="Scrape all the events. Navigate more, fetch for the full current month.",
    source="https://tockify.com/eventosemjoinville/agenda",
    config=graph_config,
    schema=EventList,
)

result = script_creator_graph.run()
print(result)
