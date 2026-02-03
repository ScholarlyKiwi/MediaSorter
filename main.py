import sys
import logging
from logging.handlers import TimedRotatingFileHandler

from src.envconfig import EnvConfig
from src.mediasorter import start_sort

environ = None

def main():
    if len(sys.argv) < 3:
        print("Usage:")
        print("     main.py - {source directory/file} {library Path} {options}")
        print("Options:")
        print("     --test_run   = testing mode that prevents moving files or saving library cache.")
        return

    print(f"Media Sorter Started.\n")

    try:
        environ = EnvConfig()

        logging.basicConfig(level=logging.INFO,
                            format="%(asctime)s %(levelname)s: %(message)s")
        environ.logger = logging.getLogger("mediasorter")
        log_handler = TimedRotatingFileHandler(environ.get_log_file(), when="D", interval=1, backupCount=7)
        formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
        log_handler.setFormatter(formatter)
        log_handler.setLevel(getattr(logging, environ.get_logging_level()))

        environ.logger.addHandler(log_handler)

        environ.set_source(sys.argv[1])
        environ.set_library(sys.argv[2])
        environ.set_test_run("--test_run" in sys.argv)

    except Exception as e:
        with open("media_sorter_exception.log", "w"):
            print("Media Sorter encoutered an error during startup:")
            print(f"{e}")

    try:
        environ.logger.debug(f"\nConfig: \n{environ}")

        start_sort(environ)
    except Exception as e:
        environ.logger.error(f"{e}")

    print("Media Sorter completed.")

if __name__ == "__main__":
    main()