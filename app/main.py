from loguru import logger
import requests
import random
from app.config.logs import ConfigLogging
from app.config.config import settings
from mangust228 import ProxyManager


def main():
    logger.info("start")
    m = ProxyManager(settings.proxy.token, settings.proxy.url)
    proxies = m.get()
    proxy = random.choice(proxies)
    logger.info(proxy)
    try:
        response = requests.get(settings.parsing.url, proxies=proxy)
        logger.log("ALERT", f"сервер поднялся [{response.status_code}]")
    except Exception as e:
        logger.info(e)


if __name__ == '__main__':
    ConfigLogging.setup()
    main()
