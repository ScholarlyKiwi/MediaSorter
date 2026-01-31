from src.envconfig import EnvConfig
import os

env = EnvConfig()

def start_sort():

    check_paths()

    if os.path.isfile(env.get_source()):
        sort_file()


def check_paths():
    validation_errors = ""
    
    if not os.path.exists(env.get_source()):
        validation_errors += f"\n * Source {env.get_source()} does not exist" 
    if not os.path.exists(env.get_library()):
        validation_errors += f"\n * Library {env.get_library()} does not exist"
    if not os.path.exists(env.get_library_base()):
        validation_errors += f"\n * Library base {env.get_library_base()} does not exist"
    if not os.path.exists(env.get_library_cache()):
        validation_errors += f"\n * Library cache {env.get_library_cache()} does not exist"

    if len(validation_errors) > 0:
        raise ValueError(validation_errors)
    return

def sort_file(path):
    return
