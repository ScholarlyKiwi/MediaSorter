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
    _update = []

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
        self._update.clear()

    def add_series(self, title, curr_season = '00', library = '', subdirectory = None):
        if title == None:
            raise Exception("Cannot add series to db without a title")
        
        if self._series_db == None:
            raise Exception(f"Cannot add series {title} - Series DB not initialised")
        
        if subdirectory == None:
            subdirectory = title.strip()

        title_file = f"{re.sub(r"[^\d\w]","_", library)}__{re.sub(r"[^\d\w]", "_",title)}___series.json"

        title_upper = title.upper()

        self._series_db[title_upper] = { "title": title,
                                "curr_season": curr_season, 
                                "library": library, 
                                "subdirectory": subdirectory,
                                "series_file": title_file}
        print(f"Adding {title_upper}")
        self._update.append(title_upper)

    def series(self, title):
        title = title.upper()
        if self._series_db == None:
            raise Exception(f"Cannot return series {title} - Series DB not initalised")
        if not self.exists(title):
            raise Exception(f"Cannot return series {title} - Series does not exist in the series DB")
        return self._series_db[title]

    def exists(self, title):
        return title.upper() in self._series_db.keys()
    
    def titles(self):
        return self._series_db.keys()

    def save_series_files(self):

        for title in self._update:

            if not self.exists(title):
                self._logger.warning(f"Attempt to save series file for series that does not exist {title}")

            series = self.series(title)
            
            series_file = series["series_file"]
            if series_file == None:
                raise Exception(f"Unable to create a filename for a series file for {title}")
            
            file_path = os.path.join(self._db_directory, series_file)

            if not os.path.exists(file_path):
                try:
                    with open(file_path, "w") as f:
                        f.write(json.dumps(series))

                except Exception as e:
                    raise (f"Unable to save series {title} file: {file_path} Reason: {e}")
        self._update.clear()
            
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

    def update_series_season(self, title, curr_season): 
        if not os.path.exists(self._db_directory):
            raise Exception(f"Cannot update series season: library cache is not initialised")
        if not self.exists(title):
            raise Exception(f"Cannot update series season: series does not exist")
        self._series_db[title.upper()]["curr_season"] = curr_season
        self._update.append(title) 