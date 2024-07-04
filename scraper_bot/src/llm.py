from litellm import completion
from loguru import logger


# Etapa 1: Ler o prompt padrão do arquivo
default_prompt_path = "prompts/yaml_generator.md"
logger.debug(f"Lendo o prompt padrão do arquivo: {default_prompt_path}")
default_prompt = open(default_prompt_path, "r").read()
logger.debug("Prompt padrão lido com sucesso.")


def llm_generate_yaml(url, html_content, query):
    # Etapa 2: Preparar a mensagem do sistema com o prompt padrão
    system_message = {"role": "system", "content": default_prompt}
    logger.debug(f"Mensagem do sistema preparada.")

    # Etapa 3: Preparar a mensagem do usuário com a URL
    url_message = {"role": "user", "content": f"url: {url}"}
    logger.debug(f"Mensagem do usuário com a URL preparada: {url_message}")

    # Etapa 4: Preparar a mensagem do usuário com o conteúdo HTML
    content_message = {"role": "user", "content": f"content: ```\n{html_content}\n```"}
    logger.debug(f"Mensagem do usuário com o conteúdo HTML preparada")

    # Etapa 5: Preparar a mensagem do usuário com a consulta
    query_message = {"role": "user", "content": f"request: ```\n{query}\n```"}
    logger.debug(f"Mensagem do usuário com a consulta preparada: {query_message}")

    # Etapa 6: Fazer a chamada à função de conclusão usando o modelo GPT-4o
    logger.debug("Fazendo a chamada à função de conclusão com as mensagens preparadas.")
    response = completion(
        model="gpt-4o",
        messages=[system_message, url_message, content_message, query_message],
    )
    logger.debug("Resposta recebida do modelo GPT-4o.")

    # Etapa 7: Extrair e retornar o conteúdo gerado pela resposta
    generated_content = response.choices[0].message.content.strip()
    logger.debug("Conteúdo gerado extraído e retornado.")
    return generated_content
