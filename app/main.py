from loguru import logger
from app.config.logs import ConfigLogging


def main():
    ...


if __name__ == '__main__':
    ConfigLogging.setup()
    logger.log("ALERT", "Start")
    main()
    logger.log("SEND_LOG_FILE", "Finish")
