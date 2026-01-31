import logging
from src.envconfig import EnvConfig

class MediaLogger():
    logger = None

    def __new__(self):
        envcon = EnvConfig()
        logger = logging.getLogger(__name__)
        logging.basicConfig(filename=envcon.get_log_file(), format='%(asctime)s %(levelname)s: %(message)s')
        logger.setLevel(getattr(logging, envcon.get_logging_level()))