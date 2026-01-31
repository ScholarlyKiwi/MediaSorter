import os
import json
import logging

class TitleAnalyzer():

    regex_db = {}

    def init_db(self, config_dir, library):
        try:
            file_path = os.path.join(config_dir, library + '_title_grep.json')
            if os.path.exists(file_path):
                file = open(file_path)
                title_config = json.load(file)
                if len(title_config) is None:
                    raise Exception("File is empty or invalid.")
                for analyzer_type in title_config:
                    info = {}
                    title = None
                    info["replacers"] = []
                    for (key, value) in analyzer_type.items():
                        match key:
                            case "title":
                                title = value
                            case _:
                                info[key] = value
                    self.regex_db[title]=info
            else:
                raise Exception("File does not exist.")
        except Exception as e:
            raise ValueError(f"Unable to read Title Analyzer config file: {file_path} for {library} error: {e} ")
        
        logging.debug(f"TitleAnalyzer = {self}")
