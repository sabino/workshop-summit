from litellm import completion

default_prompt = open("prompts/yaml_generator.md", "r").read()

def llm_generate_yaml(url, html_content, query):
    response = completion(
        model="gpt-4o",
        messages=[{"role": "system", "content": default_prompt},
                  {"role": "user", "content": f"url: {url}"},
                  {"role": "user", "content": f"content: ```\n{html_content}\n```"},
                  {"role": "user", "content": f"request: ```\n{query}\n```"}]
    )
    return response.choices[0].message.content.strip()