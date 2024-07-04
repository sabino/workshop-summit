import asyncio
from framework.llm_scrape import LLMScraper, ScraperLLMOptions
from pydantic import BaseModel, Field
from playwright.async_api import async_playwright
import json


class EventDate(BaseModel):
    start_date: str
    start_time: str
    end_date: str
    end_time: str


class Event(BaseModel):
    title: str
    date: EventDate
    description: str
    place: str
    address: str
    tags: list[str]


class EventList(BaseModel):
    events: list[Event] = Field(..., description="List of events in Joinville")


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto("https://tockify.com/eventosemjoinville/agenda")

        options = ScraperLLMOptions(
            extraction_schema=EventList,
            messages=["Extract the events happening this week in Joinville"],
            temperature=0.7,
            max_tokens=3000,
            top_p=1.0,
            mode="image",
        )

        scraper = LLMScraper(model="gpt-4o")
        result = await scraper.run(page, options)

        print(json.dumps(result.data))

        await page.close()
        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
