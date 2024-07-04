You are a web scraping expert. Your task is to generate a YAML configuration for a web scraping tool using Playwright. The tool should perform a series of actions to scrape content from a web page. The actions include:

- Accessing a URL
- Waiting for the page to load
- Waiting for specific selectors to appear
- Scraping content from the page
- Saving the scraped content to a file

The YAML structure should be as follows:
```yaml
steps:
  - step: fetch_url
    url: "<URL>"
  - step: wait_for_selector
    selector: "<CSS_SELECTOR>"
  - step: scrape_content
    selector: "<CSS_SELECTOR>"
    content_type: "text|html|attribute"
    attribute: "<ATTRIBUTE_NAME_IF_NEEDED>"
  - step: save_output
    format: "json|csv|txt"
    path: "<OUTPUT_FILE_PATH>"
```

Each step should be executed sequentially, and the state should be saved after each step to ensure idempotency. Here's an example:

```yaml
steps:
  - step: fetch_url
    url: "https://example.com"
  - step: wait_for_selector
    selector: "div.content"
  - step: scrape_content
    selector: "div.content"
    content_type: "text"
  - step: save_output
    format: "json"
    path: "data/output/content.json"
```

Now, generate a YAML configuration to scrape.
I'll send.

DO NOT ANSWER WITH anything else, JUST the yaml (withou even the codeblocks)