
from factory import ScraperFactory
from loguru import logger

destination_file = "bots/generated_config.yml"

# Etapa 1: Inicializar o ScraperFactory com o arquivo gerado
logger.debug(f"Inicializando a fábrica de scrapers com a configuração do arquivo: {destination_file}")
factory = ScraperFactory(destination_file)

# Etapa 2: Executar o scraper usando a configuração YAML gerada
logger.debug("Executando o scraper com a configuração gerada.")
factory.run()
logger.debug("Scraper executado com sucesso.")

# Etapa 3: Fechar a fábrica de scrapers
logger.debug("Fechando a fábrica de scrapers.")
factory.close()
logger.debug("Fábrica de scrapers fechada com sucesso.")
