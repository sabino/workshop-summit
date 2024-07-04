import json
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright


def fetch_page(url: str) -> str:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(url)
        content = page.content()
        browser.close()
        return content


def save_output(content: str, format: str, path: str):
    if format == "json":
        with open(path, "w") as file:
            json.dump({"content": content}, file)


def parse_html(html: str) -> BeautifulSoup:
    return BeautifulSoup(html, "html.parser")
