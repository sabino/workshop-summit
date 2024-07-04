import yaml
from playwright.sync_api import sync_playwright
from state import load_state, save_state

import json
import csv


class ScraperFactory:
    def __init__(self, config_path):
        self.config_path = config_path
        self.steps = self.load_config()
        self.state = load_state()
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=False)

    def load_config(self):
        with open(self.config_path, "r") as file:
            return yaml.safe_load(file)["steps"]

    def run(self, up_to_step=None):
        with self.browser.new_page() as page:
            for index, step in enumerate(self.steps):
                if up_to_step is not None and index > up_to_step:
                    break
                if self.state.get(f"step_{index}_done") and index != 0:
                    continue

                step_func = getattr(self, step["step"])
                step_func(page, step)
                self.state[f"step_{index}_done"] = True
                save_state(self.state)

    def fetch_url(self, page, step):
        url = step["url"]
        page.goto(url)
        self.state["current_url"] = url
        save_state(self.state)

    def wait_for_selector(self, page, step):
        selector = step["selector"]
        page.query_selector(selector)
        self.state["selector_found"] = True
        save_state(self.state)

    def scrape_content(self, page, step):
        selector = step["selector"]
        content_type = step["content_type"]
        element = page.query_selector(selector)
        if content_type == "text":
            content = element.inner_text()
        elif content_type == "html":
            content = element.inner_html()
        elif content_type == "attribute":
            attribute = step["attribute"]
            content = element.get_attribute(attribute)
        self.state["content"] = content
        save_state(self.state)

    def save_output(self, page, step):
        format = step["format"]
        path = step["path"]
        content = self.state["content"]
        if format == "json":
            with open(path, "w") as file:
                json.dump({"content": content}, file)
        elif format == "txt":
            with open(path, "w") as file:
                file.write(content)
        elif format == "csv":
            with open(path, "w") as file:
                writer = csv.writer(file)
                writer.writerow([content])

    def close(self):
        self.browser.close()
        self.playwright.stop()
