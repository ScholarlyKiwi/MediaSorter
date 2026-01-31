from configparser import ConfigParser
from src.titleanalyzer import TitleAnalyzer
from src.seriesdb import SeriesDB
import os
import sys
import logging

class EnvConfig:
    _instance = None
    _library = None
    _library_dir = None
    _source = None
    _dir_scan = None
    _log_file = None 
    _library_cache = None
    _library_base = None
    _logging_level = None
    _config_dir = None
    _ignore_directories = []
    title_analyzer = TitleAnalyzer()
    series_db = SeriesDB()
    logger = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(EnvConfig, cls).__new__(cls)
            cls._instance.config = ConfigParser()
            cls._instance.config.read('MediaSorter.ini')
        return cls._instance
    
    def __str__(cls):
        items = ""
        for section in cls._instance.config.sections():
            items += f"\n[{section}]"
            for (key, val) in cls._instance.config.items(section):
                items += f"\n   - {key}: {val}"
        return f"""    Config_Directory = {cls._config_dir}
    Dir_Scan = {cls._dir_scan}
    Library = {cls._library}
    Library_Base = {cls._library_base}
    Library_Cache = {cls._library_cache}
    Library_Dir = {cls.get_library_dir()}
    Log_File = {cls._log_file}
    Log_Level = {cls._logging_level}
    Source = {cls._source}
    --Config File--:{items}"""

    def __init__(cls):
        for section in cls._instance.config.sections():
            for (key,value) in cls._instance.config.items(section):
                match key:
                    case "log_file":
                        cls.set_log_file(value)
                    case "library_base":
                        cls.set_library_base(value)
                    case "library_cache":
                        cls.set_library_cache(value)
                    case "logging_level":
                        cls.set_logging_level(value)
                    case "config_directory":
                        cls.set_config_dir(value)
        cls.series_db.init_series_db(cls)
    
    def __format_path(cls, dir):
        try:
            if dir[0] == "/":
                #Already as absolute path
                return os.path.normpath(dir)
            elif dir[0] == "~":
                return os.path.expanduser(dir)
            else:
                return os.path.abspath(dir)
        except Exception as e:
            raise Exception(f"Invalid Path: {dir} - {e}")

    def init_title_analyzer(cls):
        cls.title_analyzer.init_db()

    def get_config_dir(cls):
        return cls.__format_path(cls._config_dir)
    
    def set_config_dir(cls, config_dir):
        cls._config_dir = config_dir

    def get_dir_scan(cls):
        return cls._dir_scan

    def set_dir_scan(cls, dir_scan):
        cls._dir_scan = dir_scan

    def get_ignore_directories(cls):
        return cls._ignore_directories.copy()

    def set_ignore_directories(cls, ignore_directories):
        cls._ignore_directories = ignore_directories.split(",")

    def get_library(cls):
        return cls._library or ''
    
    def set_library(cls, library):
        if ".." in library or "~" in library:
            raise Exception(f"Invalid library: {library}")
        cls._library = library
        if library == None:
            cls._library_dir = cls.__format_path(cls.get_library_base())
        else:
            cls._library_dir = cls.__format_path( os.path.join(cls.get_library_base(), library) )

    def get_library_base(cls):
        return cls._library_base

    def set_library_base(cls, library_base):
        cls._library_base = cls.__format_path(library_base)

    def get_library_cache(cls):
        return cls._library_cache

    def set_library_cache(cls, library_cache):
        cls._library_cache = cls.__format_path(library_cache)

    def get_library_dir(cls):
        return cls._library_dir

    def get_log_file(cls):
        return cls._log_file
    
    def set_log_file(cls, log_file):
        cls._log_file = cls.__format_path(log_file)

    def get_logging_level(cls):
        return cls._logging_level
    
    def set_logging_level(cls, logging_level):
        cls._logging_level = logging_level

    def get_source(cls):
        return cls._source

    def set_source(cls, source):
        cls._source = cls.__format_path(source)