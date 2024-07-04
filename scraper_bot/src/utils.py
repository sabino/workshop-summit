from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright


def fetch_page(url: str) -> str:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        content = page.content()
        browser.close()
        return content[:4000]


def parse_html(html: str) -> BeautifulSoup:
    return BeautifulSoup(html, "html.parser")
