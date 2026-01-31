import unittest
import logging
import json
import os

from src.seriesdb import *
from src.envconfig import EnvConfig
config = EnvConfig()

class TestSeriesDB(unittest.TestCase):

    def __init__(self, methodName = "runTest"):
        super().__init__(methodName)
        config.logger = logging.getLogger(__name__)
        logging.basicConfig(filename=config.get_log_file(), format='%(asctime)s %(levelname)s: %(message)s')
        config.logger.setLevel(getattr(logging, config.get_logging_level()))   

    def test_new_seriesdb_init_fail(self):
        with self.assertRaises(Exception) as cm:
            library_cache = SeriesDB()
            library_cache.init_series_db( None )
        self.assertEqual(str(cm.exception), "Unable to initialise series db - config not found.") 

    def test_new_seriesdb_init_bad_dir(self):
        temp = config.get_library_cache()
        config.set_library_cache('bonk')
        with self.assertRaises(Exception) as cm:
            library_cache = SeriesDB()
            library_cache.init_series_db( config )
        self.assertEqual(str(cm.exception), "Configuration Error - library cache directory is invalid: /home/david/Programming/projects/MediaSorter/bonk")
        config.set_library_cache(temp)

    def test_new_seriesdb(self):
        library_cache = SeriesDB()
        library_cache.init_series_db(config)
        self.assertIsNotNone(library_cache)

    def test_add_series_fail(self):
        library_cache = SeriesDB()
        library_cache.init_series_db(config)
        expected_results = "Cannot add series to db without a title"

        with self.assertRaises(Exception) as cm:
            library_cache.add_series(None, None, None, None)
        
        self.assertEqual(str(cm.exception), expected_results)

    def test_add_exists_series(self):
        library_cache = SeriesDB()
        library_cache.init_series_db(config)
        library_cache.add_series("test", 1, "anime", "test")
        self.assertTrue(library_cache.exists("test"))

    def test_add_not_exists_series(self):
        library_cache = SeriesDB()
        library_cache.init_series_db(config)
        library_cache.add_series("test", 1, "anime", "test")
        self.assertFalse(library_cache.exists("test2"))

    def test_return_series(self):
        library_cache = SeriesDB()
        library_cache.init_series_db(config)
        library_cache.add_series("test_title", 1, "anime_library", "test_subdirectory")
        expected = {'curr_season': 1, 'library': 'anime_library', 'subdirectory': 'test_subdirectory', 'series_file': 'anime_library__test_title___series.json', 'title': 'test_title'}
        result = library_cache.series("test_title")
        self.assertEqual(expected, result)

    def test_add_return_series_no_subdir_(self):
        library_cache = SeriesDB()
        library_cache.init_series_db(config)
        library_cache.add_series("test_title", 1, "anime_library")
        expected = {'curr_season': 1, 'library': 'anime_library', 'subdirectory': 'test_title', 'series_file': 'anime_library__test_title___series.json', 'title': 'test_title'}
        result = library_cache.series("test_title")
        self.assertEqual(expected, result)

    def test_add_return_series_comma(self):
        library_cache = SeriesDB()
        library_cache.init_series_db(config)
        library_cache.add_series("test'title", 1, "anime_library")
        expected = {'curr_season': 1, 'library': 'anime_library', 'subdirectory': 'test_title', 'series_file': 'anime_library__test_title___series.json', 'title': 'test\'title'}
        result = library_cache.series("test'title")
        self.assertEqual(expected, result)

    def test_save_db_one_file(self):
        library_cache = SeriesDB()
        library_cache.init_series_db(config)
        library_cache.add_series("test_title", 1, "anime_library", "test_subdirectory")
        library_cache.save_series_db()
        self.assertTrue(os.path.exists("/home/david/Programming/projects/MediaSorter/library_cache/anime_library__test_title___series.json"))

    def test_save_db_three_file(self):
        library_cache = SeriesDB()
        library_cache.init_series_db(config)
        library_cache.add_series("test_title", 1, "anime_library", "test_subdirectory")
        library_cache.add_series("test_3", "1", "anime_3", "subdir_3")
        library_cache.add_series("test_2", 3, "anime_2", "subdir_2")
        library_cache.save_series_db()
        files_save = True
        base_path = "/home/david/Programming/projects/MediaSorter/library_cache/"
        for title in library_cache.titles():
            series = library_cache.series(title)
            file_path = os.path.join(base_path, series['series_file'])
            if not os.path.exists(file_path):
                files_save = False
        self.assertTrue(files_save)

    def test_save_db_three_file(self):
        library_cache = SeriesDB()
        library_cache.init_series_db(config)
        library_cache.add_series("test_title", 1, "anime_library", "test_subdirectory")
        library_cache.add_series("test_3", "1", "anime_3", "subdir_3")
        library_cache.add_series("test_2", 3, "anime_2", "subdir_2")
        library_cache.save_series_db()

        found_files = True
        base_path = "/home/david/Programming/projects/MediaSorter/library_cache/"
        json_str = ""
        result_str = ""

        for title in library_cache.titles():
            series = library_cache.series(title)
            file_path = os.path.join(base_path, series['series_file'])
            result_str += str(series)
            if not os.path.exists(file_path):
                found_files = False
            else:
                with open(file_path) as f:
                    json_str += str(json.load(f))

        self.assertTrue(found_files)
        self.assertEqual(json_str, result_str)

    def test_load_db(self):
        library_cache = SeriesDB()
        library_cache.init_series_db(config)
        library_cache.load_series_files()
