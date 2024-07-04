from factory import ScraperFactory
from llm import llm_generate_yaml
from utils import fetch_page
from loguru import logger

# Configuração do logger
logger.add("debug.log", format="{time} {level} {message}", level="DEBUG", rotation="1 MB")

destination_file = "bots/generated_config.yml"

# Etapa 1: Buscar o conteúdo HTML inicial (conteúdo HTML de exemplo)
url = "https://example.com"
logger.debug(f"Buscando o conteúdo HTML da URL: {url}")
html_content = fetch_page(url)
logger.debug("Conteúdo HTML buscado com sucesso.")

# Etapa 2: Definir a consulta para extração
query = "Extrair o título da página"
logger.debug(f"Consulta definida para extração: {query}")

# Etapa 3: Gerar a configuração YAML usando GPT-4
yaml_config = llm_generate_yaml(url, html_content, query)
logger.debug("Configuração YAML gerada com sucesso usando GPT-4.")

# Etapa 4: Salvar a configuração YAML
logger.debug(f"Salvando a configuração YAML no arquivo: {destination_file}")
with open(destination_file, "w") as file:
    file.write(yaml_config)
logger.debug("Configuração YAML salva com sucesso.")

# Etapa 5: Inicializar a fábrica de scrapers com a configuração YAML gerada
logger.debug(f"Inicializando a fábrica de scrapers com a configuração do arquivo: {destination_file}")
factory = ScraperFactory(destination_file)

# Etapa 6: Executar o scraper usando a configuração YAML gerada
logger.debug("Executando o scraper com a configuração gerada.")
factory.run()
logger.debug("Scraper executado com sucesso.")

# Etapa 7: Fechar a fábrica de scrapers
logger.debug("Fechando a fábrica de scrapers.")
factory.close()
logger.debug("Fábrica de scrapers fechada com sucesso.")
