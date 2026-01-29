from configparser import ConfigParser

class EnvConfig:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(EnvConfig, cls).__new__(cls)
            cls._instance.config = ConfigParser()
            cls._instance.config.read('MediaSorter.ini')
            cls._instance.library = None
            cls._instance.source = None
        return cls._instance
    
    def __str__(cls):
        items = ""
        for section in cls._instance.config.sections():
            items += f"\n[{section}]"
            for (key, val) in cls._instance.config.items(section):
                items += f"\n   - {key}: {val}"
        return f"\nLibrary = {cls._instance.library}\nSource = {cls._instance.source}\n--EnvConfig--:{items}"

    def set_source(cls, source):
        cls._instance.source = source

    def set_library(cls, library):
        cls._instance.library = library


if __name__ == "__main__":
    main()