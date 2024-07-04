from scrapegraphai.graphs import ScriptCreatorGraph
from pydantic import BaseModel, Field
from os import environ


class Book(BaseModel):
    title: str
    price: str
    thumb_url: str


class BookList(BaseModel):
    books: list[Book] = Field(..., description="List of books")


graph_config = {
    "llm": {
        "api_key": environ["OPENAI_API_KEY"],
        "model": "gpt-4o",
        "temperature": 0,
    },
    "library": "playwright",
    "headless": False,
    "verbose": False,
    "burr_kwargs": {
        "project_name": "test-scraper",
        "app_instance_id": "some_id",
    },
}

script_creator_graph = ScriptCreatorGraph(
    prompt="Create a Python script to Scrape all the books.",
    source="https://books.toscrape.com/",
    config=graph_config,
    schema=BookList,
)

result = script_creator_graph.run()
print(result)
