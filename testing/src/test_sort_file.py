import unittest
import logging

from src.mediasorter import *
from src.envconfig import EnvConfig
config = EnvConfig()

class TestSortFile(unittest.TestCase):

    def __init__(self, methodName = "runTest"):
        super().__init__(methodName)
        config.logger = logging.getLogger(__name__)
        logging.basicConfig(filename=config.get_log_file(), format='%(asctime)s %(levelname)s: %(message)s')
        config.logger.setLevel(getattr(logging, config.get_logging_level()))       

    def test_sort_file(self):
        source = "~/Videos/Downloads/[ASW] Tensei shitara Dragon no Tamago datta - 03 [1080p HEVC][AD2A35FA].mkv"
        sort_file(source, config)

    def test_sort_directory(self):
        source = "~/Videos/Downloads/"
        # config.logger = logging.getLogger(__name__)
        # logging.basicConfig(filename=config.get_log_file(), format='%(asctime)s %(levelname)s: %(message)s')
        # config.logger.setLevel(getattr(logging, config.get_logging_level()))
        config.set_source(source)

        sort_directory(config.get_source(), config)
