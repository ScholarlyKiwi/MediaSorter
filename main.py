import sys
from src.envconfig import EnvConfig

def main():
    print(f"Staring Media Sorter.")

    environ = EnvConfig()
    # Arguments :
    # 0) Source Directory/File
    # 1) Base Library Directory

    if len(sys.argv) < 3:
        print("Usage:")
        print(" main.py - {source directory/file} {Library Path}")
        return
    
    environ.set_source(sys.argv[1])
    environ.set_library(sys.argv[2])

    print(f"Config {environ}")
    

if __name__ == "__main__":
    main()