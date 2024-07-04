import asyncio
from framework.llm_scrape import LLMScraper, ScraperLLMOptions
from playwright.async_api import async_playwright
from pydantic import BaseModel, Field


class Story(BaseModel):
    title: str
    points: int
    by: str
    commentsURL: str


class TopStories(BaseModel):
    top: list[Story] = Field(..., description="Top 5 stories on Hacker News")


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto("https://news.ycombinator.com")

        options = ScraperLLMOptions(
            extraction_schema=TopStories,
            messages=["Extract the top 5 stories on Hacker News"],
            temperature=0.7,
            max_tokens=3000,
            top_p=1.0,
            mode="html",
        )

        scraper = LLMScraper(model="gpt-4o")
        result = await scraper.run(page, options)

        print(result.data)

        await page.close()
        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
