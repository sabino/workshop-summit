from factory import ScraperFactory
from llm import llm_generate_yaml
from utils import fetch_page

def main():
    # Fetch initial HTML content (placeholder for actual HTML content)
    url = "https://example.com"
    html_content = fetch_page(url)
    query = "Extract the title of the page"
    
    # Generate YAML configuration using GPT-4
    yaml_config = llm_generate_yaml(url, html_content, query)
    
    # Save the YAML configuration
    with open('bots/generated_config.yml', 'w') as file:
        file.write(yaml_config)
    
    # Execute the scraper using the generated YAML configuration
    factory = ScraperFactory('bots/generated_config.yml')
    factory.run()
    factory.close()

if __name__ == "__main__":
    main()
