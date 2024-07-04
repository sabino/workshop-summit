import asyncio
from pydantic import BaseModel, Field
from playwright.async_api import async_playwright
import litellm
import html2text
from readability import Document
import json


class ScraperLoadResult(BaseModel):
    url: str
    content: str
    mode: str


class ScraperLLMOptions(BaseModel):
    extraction_schema: type[BaseModel]
    system_prompt: str = (
        "You are a sophisticated web scraper. Extract the contents of the webpage and return JSON."
        " You should NEVER reply anything other than JSON. Do not include anything other than the extracted data in your response."
        " NOT EVEN CODE BLOCKS. Just json."
    )
    messages: list[str] = Field(default_factory=list)
    temperature: float = 0.7
    max_tokens: int = 100
    top_p: float = 1.0
    mode: str = "html"  # Add the mode attribute here


class ScraperCompletionResult(BaseModel):
    data: dict | None
    url: str


async def preprocess(page, mode: str = "html") -> ScraperLoadResult:
    url = page.url
    content = ""

    if mode == "html":
        content = await page.content()
    elif mode == "markdown":
        body = await page.inner_html("body")
        content = html2text.html2text(body)
    elif mode == "text":
        html_content = await page.content()
        doc = Document(html_content)
        content = f"Page Title: {doc.title()}\n{doc.summary()}"
    elif mode == "image":
        image = await page.screenshot()
        content = image.decode("base64")

    return ScraperLoadResult(url=url, content=content, mode=mode)


async def generate_completions(
    page: ScraperLoadResult, options: ScraperLLMOptions
) -> ScraperCompletionResult:
    # Convert the schema to a JSON string
    schema_str = json.dumps(options.extraction_schema.model_json_schema())
    messages = [{"role": "system", "content": options.system_prompt}]
    messages.append({"role": "user", "content": f"Schema:\n{schema_str}"})
    messages.append({"role": "user", "content": page.content})

    # Add any additional messages provided in the options
    for msg in options.messages:
        messages.append({"role": "user", "content": msg})

    response = litellm.completion(
        model="gpt-4o",
        messages=messages,
        temperature=options.temperature,
        max_tokens=options.max_tokens,
        top_p=options.top_p,
    )
    result = json.loads(response.choices[0].message["content"].strip())
    return ScraperCompletionResult(data=result, url=page.url)


class LLMScraper:
    def __init__(self, model: str):
        self.model = model

    async def run(self, page, options: ScraperLLMOptions):
        preprocessed = await preprocess(page, options.mode)
        return await generate_completions(preprocessed, options)


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto("https://news.ycombinator.com")

        class Story(BaseModel):
            title: str
            points: int
            by: str
            commentsURL: str

        class TopStories(BaseModel):
            top: list[Story] = Field(..., description="Top 10 stories on Hacker News")

        options = ScraperLLMOptions(
            extraction_schema=TopStories,
            messages=["Extract the top 10 stories on Hacker News"],
            temperature=0.7,
            max_tokens=3000,
            top_p=1.0,
            mode="html",
        )

        scraper = LLMScraper(model="gpt-4o")
        result = await scraper.run(page, options)

        print(json.dumps(result.data))

        await page.close()
        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
