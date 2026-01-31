from src.seriesdb import SeriesDB
import os
import re
import shutil


def start_sort(config):

    config.logger.debug(f"Starting Sort Process.")

    check_paths(config)
    config.title_analyzer.init_db(config.get_config_dir(), config.get_library())
    
    source = config.get_source()

    if os.path.isfile(source):
        sort_file(source, config)
    elif os.path.isdir(source):
        sort_directory(source, config)
    else:
        raise Exception(f"")


def check_paths(config):
    validation_errors = ""
    if not os.path.exists(config.get_source()):
        validation_errors += f"\n * Source {config.get_source()} does not exist" 
    if not os.path.exists(config.get_library_dir()):
        validation_errors += f"\n * Library {config.get_library_dir()} does not exist"
    if not os.path.exists(config.get_library_base()):
        validation_errors += f"\n * Library base {config.get_library_base()} does not exist"
    if not os.path.exists(config.get_library_cache()):
        validation_errors += f"\n * Library cache {config.get_library_cache()} does not exist"
    if not os.path.exists(config.get_config_dir()):
        validation_errors += f"\n * Configuration {config.get_library()} does not exist"

    if len(validation_errors) > 0:
        raise ValueError(validation_errors)
    return

def sort_file(path, config):
    series_title = None
    episode = None
    replacers = None
    season = None
    
    file_name = os.path.basename(path)
    file_tuple = os.path.splitext(file_name)
    split_name = file_tuple[0]
    
    episode_info = None
    title_regex = config.title_analyzer.regex_db.copy()
    series_db = config.series_db

    config.logger.debug(f"Beginning Analysis - {file_name}")
    for regex_type in title_regex.keys():
        episode_info = get_episode_info(split_name, title_regex[regex_type])
        if episode_info != None:
            if episode_info[0] != None and episode_info[1] != None:
                series_title = episode_info[0]
                episode = episode_info[1]
                season = episode_info[2]
                replacers = title_regex[regex_type]["replacers"]
                break

    if episode_info == None:
        config.logger.warning(f"Title in unknown format: {file_name}")
        return

    if series_title == None or episode == None :
        config.logger.warning(f"Unable to determine episode details for {file_name}\nseries = {series_title}, episode = {episode}, season = {season}")
        return

    # If the episode info didn't return a season, fall back to the series db.
    if season == None:
        if series_db.exists(series_title):
            season = series_db.series(series_title)["curr_season"]
        
        if season == None:
            # if we still can't figure out the season, assume season 00.
            season = "00"

    if not series_db.exists(series_title):
        series_db.add_series(series_title, library=config.get_library())
        series_db.save_series_file(series_title)
    
    config.logger.debug(f"\n    file_name = {file_name}\n    series = {series_title}\n    episode = {episode}\n    season = {season}\n    replacers = {replacers}")

    dest_file_name = file_name
    if len(replacers) > 0:
        for replacer in replacers:
            pattern = replacer["pattern"]
            remover = replacer["remover"]       
            replace = replacer["replace"]
            if pattern == None:
                raise ValueError(f"Missing Replacer pattern in {replacers}")
            if replace == None:
                raise ValueError(f"Missing replace string in {replacers} ")
            

            formatted_pattern = pattern.format(episode=episode, series=series_title, season=season)
            episode_removed = formatted_pattern.replace(remover, '')

            formatted_replace = replace.format(episode=episode_removed, series=series_title, season=season)

            dest_file_name = file_name.replace(formatted_pattern, formatted_replace)

    dest_path = os.path.join(config.get_library_dir(), series_db.series(series_title)["subdirectory"])
    
    try:
        if not os.path.exists(dest_path) and dest_path != None:
            os.makedirs(dest_path, exist_ok=True)
    except Exception as e:
        raise Exception(f"Unable to create new series directory at {dest_path}")
    
    print(f"dest_path = {dest_path}, dest_file_name = {dest_file_name}")
    dest_path = os.path.join(dest_path, dest_file_name)

    print(f"dest_path = {dest_path}, dest_file_name = {dest_file_name}")

    config.logger.info(f"Moving {file_name} to {dest_path}")
    if dest_path == None:
        raise Exception(f"Lost the destination for {file_name}")
    try:
        dest = shutil.move(path, dest_path)
        print(f"Moved to {dest}")
    except Exception as e:
        raise Exception(f"Error moving {file_name} - {e}")
    return

def get_episode_info(title, regex_db_obj):
    series_title = None
    episode = None
    season = None
    try:
        regex_string = regex_db_obj["regex"]
        title_reg = re.compile(regex_string)
        
        regex_match = title_reg.match(title)
        title_groups = regex_db_obj["groups"].split(',')

        if regex_match == None:
            return None    
        else:
            index = 0
            if regex_match.groups() == None:
                return None
            while index < len(title_groups):
                if regex_match.groups()[index] != None:
                    key = title_groups[index].lower().strip()
                    temp_season = None
                    temp_episode = None
                    match key:
                        case "title":
                            series_title = regex_match.groups()[index]
                        case "episode":
                            temp_episode = regex_match.groups()[index]
                        case "seasonepisode":
                            # seasonepisdoe is the format S##E##
                            # retrieve the season in case we need it
                            temp = regex_match.groups()[index].strip()
                            temp_season = temp[1:3]
                            temp_episode = temp[-2:]
                        case "season":
                            temp_season = regex_match.groups()[index]
                    if temp_episode != None and episode == None:
                        episode = temp_episode
                    if temp_season != None and season == None:
                        season = temp_season 
                index += 1

    except Exception as e:
        raise ValueError(f"Error analyzing edisode info: {title} {e}")
                    
    result = (series_title, episode, season) 
    return result

def sort_directory(source, config):
    
    config.logger.debug(f"Start Directory Sorting: {source}")
    dir_contents = os.listdir(source)
    
    for object in dir_contents:
        object_path = os.path.join(source, object)
        if os.path.isdir(object_path):
            if not object_path in config.get_ignore_directories():
                sort_directory(object_path, config)
        elif os.path.isfile(object_path):
            sort_file(object_path, config)