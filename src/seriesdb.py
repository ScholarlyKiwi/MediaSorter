import json
import os
import re
from pathlib import Path

class SeriesDB():

    _instance = None
    _series_db = None
    _logger = None
    _db_directory = None
    _library = None

    def __new__(self):
        if self._instance is None:
            self._instance = super(SeriesDB, self).__new__(self)
        return self._instance

    def init_series_db(self, config):
        if config == None:
            raise Exception("Unable to initialise series db - config not found.")
        self._series_db = {}
        self._logger = config.logger
        self._library = config.get_library()

        norm_db_directory = os.path.normpath(config.get_library_cache())
        if os.path.exists(norm_db_directory) and os.path.isdir(norm_db_directory):
            self._db_directory = norm_db_directory
        else:
            raise Exception(f"Configuration Error - library cache directory is invalid: {norm_db_directory}")

    def add_series(self, title, curr_season = '00', library = '', subdirectory = None):
        if title == None:
            raise Exception("Cannot add series to db without a title")
        
        if self._series_db == None:
            raise Exception(f"Cannot add series {title} - Series DB not initialised")
        
        if subdirectory == None:
            subdirectory = title.strip()

        title_file = f"{re.sub(r"[^\d\w]","_", library)}__{re.sub(r"[^\d\w]", "_",title)}___series.json"

        self._series_db[title.upper()] = { "title": title,
                                "curr_season": curr_season, 
                                "library": library, 
                                "subdirectory": subdirectory,
                                "series_file": title_file}

    def series(self, title):
        if self._series_db == None:
            raise Exception(f"Cannot return series {title} - Series DB not initalised")
        if not self.exists(title.upper()):
            raise Exception(f"Cannot return series {title} - Series does not exist in the series DB")
        return self._series_db[title.upper()]

    def exists(self, title):
        return title.upper() in self._series_db
    
    def titles(self):
        return self._series_db.keys()

    def save_series_db(self):
        for title in self._series_db.keys():
            self.save_series_file(title)

    def save_series_file(self, title):
        if not self.exists(title):
            self._logger.warning(f"Attempt to update series file for series that does not exist {title}")
        series = self.series(title)
        
        series_file = series["series_file"]
        if series_file == None:
            raise Exception(f"Unable to create a name for a series file for {title}")
        
        file_path = os.path.join(self._db_directory, series_file)
        # There isn't a way for the series to be updated in the script so the data in the
        # files should be the same or newer than the data stored in the series DB. So only
        # write new files.
        if not os.path.exists(file_path):
            try:
                with open(file_path, "w") as f:
                    f.write(json.dumps(series))

            except Exception as e:
                raise (f"Unable to save series {title} file: {file_path} Reason: {e}")
            
    def load_series_files(self):
        if not os.path.exists(self._db_directory):
            raise Exception(f"Unable to load series files library cache directory invalid - {self._db_directory}")
        if not os.path.isdir(self._db_directory):
            raise Exception(f"Unable to load series files library cache is not a directory - {self._db_directory}")
        
        library_pattern = f"{self._library}*.json"
        for object in Path(self._db_directory).glob(library_pattern):
            file_path = os.path.join(self._db_directory, object)
            with open(file_path, 'r') as f:
                series = json.load(f)
                self._series_db[series["title"]] = series
