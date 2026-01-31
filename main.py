import sys
import logging

from src.envconfig import EnvConfig
from src.mediasorter import start_sort
from src.medialogger import MediaLogger

logger = logging.getLogger(__name__)
environ = EnvConfig()

def main():
    print(f"Staring Media Sorter.")

    try:
        logging.basicConfig(filename=environ.get_log_file(), format='%(asctime)s %(levelname)s: %(message)s')
        logger.setLevel(getattr(logging, environ.get_logging_level()))
    except Exception as e:
        with open("media_sorter_exception.log", "w"):
            print("Media Sorter encoutered an error during startup:")
            print(f"{e}")

    # Arguments :
    # 0) Source Directory/File
    # 1) Base Library Directory
    try:
        if len(sys.argv) < 3:
            print("Usage:")
            print("     main.py - {source directory/file} {library Path} {options}")
            print("Options:")
            print("     --dir_scan   = sorts all files and directories in the source directory.")
            return
        
        environ.set_source(sys.argv[1])
        environ.set_library(sys.argv[2])

        environ.set_dir_scan("--dir_scan" in sys.argv)
        logger.debug(f"\nConfig: \n{environ}")
        start_sort()
    except Exception as e:
        logging.error(f"{e}")
    

if __name__ == "__main__":
    main()