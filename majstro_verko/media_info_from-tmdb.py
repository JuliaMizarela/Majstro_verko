from pathlib import Path
import csv
import requests
import json


def get_movie_titles_from_csv(movies_csv_path: str = None) -> list:
    if movies_csv_path is None:
        movies_csv_path = r'majstro_verko/Files/movies_basic_info_from_tmdb.csv'
        with open(movies_csv_path, newline='\n', mode='r', encoding='utf-8-sig') as csv_file:
            reader = csv.DictReader(csv_file, delimiter=',', dialect='unix')
            list_of_movies_titles = [row['original_title'] for row in reader if row['original_title'] != '' ]
    else:
        with open(movies_csv_path, newline='\n', mode='r', encoding='utf-8-sig') as csv_file:
            reader = csv.DictReader(csv_file, delimiter=',', dialect='unix')
            list_of_movies_titles = [row['title'] for row in reader if row['title'] != '' ]
    return list_of_movies_titles


def download_movies_tmdb_jsons_from_titles_list(movies_titles: list, movies_csv_path: str = None, api_keys_path: str = None):
    headers = {'Accept': 'application/json'}
    correctly_named_json_paths = []
    if movies_csv_path is None:
        movies_csv_path = r'majstro_verko/Files/movies_basic_info_from_tmdb.csv'
    if api_keys_path is None:
        api_key = Path(r'API_keys/TMDB_API_Key.txt').read_text().strip()
    for movie_title in movies_titles:
        api_url = f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&language=en-US&query={movie_title}&page=1&include_adult=false"
        response = requests.get(api_url, headers=headers)
        with open(f'majstro_verko/Files/Movies_jsons/{movie_title}.json', 'wb') as outf:
            outf.write(response.content)
        if parse_json_from_list_of_files([f'majstro_verko/Files/Movies_jsons/{movie_title}.json'])[0]['results']:
            correctly_named = parse_json_from_list_of_files([f'majstro_verko/Files/Movies_jsons/{movie_title}.json'])[0]['results'][0]['original_title']
            correctly_named_json_paths.append(f'majstro_verko/Files/Movies_jsons/{correctly_named}.json')
            with open(f'majstro_verko/Files/Movies_jsons/{correctly_named}.json', 'wb') as outf:
                outf.write(response.content)
    return list(correctly_named_json_paths)


def download_movies_tmdb_jsons_from_titles_csv(movies_csv_path: str = None, api_keys_path: str = None):
    headers = {'Accept': 'application/json'}
    if movies_csv_path is None:
        movies_csv_path = r'majstro_verko/Files/movies_basic_info_from_tmdb.csv'
    if api_keys_path is None:
        api_key = Path(r'API_keys/TMDB_API_Key.txt').read_text().strip()
    list_of_movies_titles = get_movie_titles_from_csv(movies_csv_path)
    for movie_title in list_of_movies_titles:
        api_url = f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&language=en-US&query={movie_title}&page=1&include_adult=false"
        response = requests.get(api_url, headers=headers)
        with open(f'majstro_verko/Files/Movies_jsons/{movie_title}.json', 'wb') as outf:
            outf.write(response.content)
        if parse_json_from_list_of_files([f'majstro_verko/Files/Movies_jsons/{movie_title}.json'])[0]['results']:
            correctly_named = parse_json_from_list_of_files([f'majstro_verko/Files/Movies_jsons/{movie_title}.json'])[0]['results'][0]['original_title']
            with open(f'majstro_verko/Files/Movies_jsons/{correctly_named}.json', 'wb') as outf:
                outf.write(response.content)


def parse_json_from_list_of_files(json_names_with_path: list = None, csv_of_titles = None) -> list:
    if json_names_with_path is None:
        list_of_movies_titles = get_movie_titles_from_csv(csv_of_titles)
        json_names_with_path = [f'majstro_verko/Files/Movies_jsons/{movie_title}.json' for movie_title in list_of_movies_titles]
    parsed_json = [json.load(Path(json_path).open()) for json_path in json_names_with_path]
    return parsed_json


def save_movie_basic_info_to_csv(destination_path: str = None, list_of_json_files: list = None, csv_of_titles: str = None):
    if list_of_json_files is None:
        if csv_of_titles is None:
            parsed = parse_json_from_list_of_files(csv_of_titles=r'majstro_verko/Files/movies.csv')
        else:
            parsed = parse_json_from_list_of_files(csv_of_titles=csv_of_titles)
        write_mode = 'w'
    else:
        parsed = parse_json_from_list_of_files(json_names_with_path=list_of_json_files)
        write_mode = "a+"
    movies_basic_info = [{'title': movie['results'][0]['title'], 'original_title': movie['results'][0]['original_title'], 'year': movie['results'][0]['release_date'][:4]} for movie in parsed if movie['results']]
    if destination_path is None:
        destination_path = r'majstro_verko/Files/movies_basic_info_from_tmdb.csv'
    with open(destination_path, write_mode) as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=["title", "original_title", "year"], dialect="unix")
        if write_mode == 'w': writer.writeheader()
        for movie in movies_basic_info:
            writer.writerow(movie)


def save_all_movie_info_to_csv(destination_path: str = None, list_of_json_files: list = None):
    if list_of_json_files is None:
        parsed = parse_json_from_list_of_files()
        write_mode = 'w'
    else:
        parsed = parse_json_from_list_of_files(json_names_with_path=list_of_json_files)
        write_mode = "a+"
    available_info = list(parsed[0]['results'][0])
    movies_basic_info = [{key: movie['results'][0][key] for key in available_info if key in list(movie['results'][0].keys())} for movie in parsed if movie['results']]
    if destination_path is None:
        destination_path = r'majstro_verko/Files/all_movies_info_from_tmdb.csv'
    with open(destination_path, write_mode) as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=available_info, dialect="unix")
        if write_mode == 'w': writer.writeheader()
        for movie in movies_basic_info:
            writer.writerow(movie)


def try_and_correct_for_wrong_hits(destination_path: str = None):
    wrong_hits_path = r'majstro_verko/Files/wrong_hits.txt'
    if Path(wrong_hits_path).is_file() and Path(wrong_hits_path).stat().st_size:
        wrong_hits_list = Path(wrong_hits_path).read_text().split('\n')
        wrong_hits_path_list = [entry.split("|")[0] for entry in wrong_hits_list]
        wrong_hits_json_key_list = [int(entry.split("|")[1]) for entry in wrong_hits_list]
        list_of_wrong_hits_paths = [r'majstro_verko/Files/Movies_jsons/'+name for name in wrong_hits_path_list]
        parsed = parse_json_from_list_of_files(list_of_wrong_hits_paths)
        available_info = list(parsed[0]['results'][0] )
        all_movies_info = [{key: parsed[i]['results'][wrong_hits_json_key_list[i]][key] for key in available_info} for i in range(0, len(parsed)) if parsed[i]['results']]
        if destination_path is None:
            destination_path = r'majstro_verko/Files/all_movies_info_from_tmdb.csv'
        with open(destination_path, 'a+') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=available_info, dialect="unix")
            for movie in all_movies_info:
                writer.writerow(movie)


def get_movies_ids_from_json_paths(json_paths: list):
    parsed = parse_json_from_list_of_files(json_paths)
    movies_ids = [movie['results'][0]['id'] if len(parsed) > 1 else parsed[0]['results'][0]['id'] for movie in parsed ]
    return movies_ids



def get_movies_simplified_credits(csv_with_all_tmdb_info: str = None, target_csv: str = None, movies_ids: list = None):
    headers = {'Accept': 'application/json'}
    write_mode = 'a+'
    if csv_with_all_tmdb_info is None:
        csv_with_all_tmdb_info = r'majstro_verko/Files/all_movies_info_from_tmdb.csv'
    if target_csv is None:
        target_csv = r'majstro_verko/Files/movies_simplified_credits_from_tmdb.csv'
    if movies_ids is None:
        with open(csv_with_all_tmdb_info, newline='\n', mode='r', encoding='utf-8-sig') as csv_input_file:
            reader = csv.DictReader(csv_input_file, dialect="unix")
            movies_ids = [row['id'] for row in reader]
        write_mode = 'w'
    with open(target_csv, newline='\n', mode=write_mode, encoding='utf-8-sig') as csv_output_file:
        simplified_credits_header = ["movie_id","director_1", "director_2", "writer_1", "writer_2", "editor_1", "editor_2", "producer_1", "producer_2", "composer_1", "main_actor_1", "main_character_1", "main_actor_2", "main_character_2", "main_actor_3", "main_character_3"]
        writer = csv.DictWriter(csv_output_file, fieldnames=simplified_credits_header)
        if write_mode == 'w': writer.writeheader()
        for movie_id in movies_ids:
            api_url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key=d3cb2b808d78860b359603d4a283c60f&language=en-US"
            response = requests.get(api_url, headers=headers)
            parsed_response = json.loads(response.content)
            writer.writerow({"movie_id": movie_id,
            "director_1": [crew['name'] for crew in parsed_response['crew'] if crew['job'] == 'Director'][0] if len([crew['name'] for crew in parsed_response['crew'] if crew['job'] == 'Director']) >= 1 else "",
            "director_2": [crew['name'] for crew in parsed_response['crew'] if crew['job'] == 'Director'][1] if len([crew['name'] for crew in parsed_response['crew'] if crew['job'] == 'Director']) > 1 else "", 
            "writer_1": [crew['name'] for crew in parsed_response['crew'] if crew['job'] == 'Screenplay'][0] if len([crew['name'] for crew in parsed_response['crew'] if crew['job'] == 'Screenplay']) >= 1 else "",
            "writer_2": [crew['name'] for crew in parsed_response['crew'] if crew['job'] == 'Screenplay'][1] if len([crew['name'] for crew in parsed_response['crew'] if crew['job'] == 'Screenplay']) > 1 else "",
            "editor_1": [crew['name'] for crew in parsed_response['crew'] if crew['job'] == 'Editor'][0] if len([crew['name'] for crew in parsed_response['crew'] if crew['job'] == 'Editor']) >= 1 else "",
            "editor_2": [crew['name'] for crew in parsed_response['crew'] if crew['job'] == 'Editor'][1] if len([crew['name'] for crew in parsed_response['crew'] if crew['job'] == 'Editor']) > 1 else "",
            "producer_1": [crew['name'] for crew in parsed_response['crew'] if crew['job'] == 'Producer'][0] if len([crew['name'] for crew in parsed_response['crew'] if crew['job'] == 'Producer']) >= 1 else "",
            "producer_2": [crew['name'] for crew in parsed_response['crew'] if crew['job'] == 'Producer'][1] if len([crew['name'] for crew in parsed_response['crew'] if crew['job'] == 'Producer']) > 1 else "",
            "composer_1": [crew['name'] for crew in parsed_response['crew'] if crew['job'] == 'Original Music Composer'][0] if len([crew['name'] for crew in parsed_response['crew'] if crew['job'] == 'Original Music Composer']) >= 1 else "",
            "main_actor_1": parsed_response['cast'][0]['name'] if len(parsed_response['cast']) >= 1 else "",
            "main_character_1": parsed_response['cast'][0]['character'] if len(parsed_response['cast']) >= 1 else "",
            "main_actor_2": parsed_response['cast'][1]['name'] if len(parsed_response['cast']) >= 2 else "",
            "main_character_2": parsed_response['cast'][1]['character'] if len(parsed_response['cast']) >= 2 else "",
            "main_actor_3": parsed_response['cast'][2]['name'] if len(parsed_response['cast']) >= 3 else "",
            "main_character_3": parsed_response['cast'][2]['character'] if len(parsed_response['cast']) >= 3 else ""
            })


def get_movies_runtime(csv_with_all_tmdb_info: str = None, target_csv: str = None, movies_ids = None):
    headers = {'Accept': 'application/json'}
    write_mode = 'a+'
    if csv_with_all_tmdb_info is None:
        csv_with_all_tmdb_info = r'majstro_verko/Files/all_movies_info_from_tmdb.csv'
    if target_csv is None:
        target_csv = r'majstro_verko/Files/movies_runtime_from_tmdb.csv'
    if movies_ids is None:
        with open(csv_with_all_tmdb_info, newline='\n', mode='r', encoding='utf-8-sig') as csv_input_file:
            reader = csv.DictReader(csv_input_file, dialect="unix")
            movies_ids = [row['id'] for row in reader]
        write_mode = 'w'
    with open(target_csv, newline='\n', mode=write_mode, encoding='utf-8-sig') as csv_output_file:
        runtime_header = ["movie_id","runtime"]
        writer = csv.DictWriter(csv_output_file, fieldnames=runtime_header)
        if write_mode == 'w': writer.writeheader()
        for movie_id in movies_ids:
            api_url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=d3cb2b808d78860b359603d4a283c60f&language=en-US"
            response = requests.get(api_url, headers=headers)
            parsed_response = json.loads(response.content)
            writer.writerow({"movie_id": movie_id, "runtime": parsed_response['runtime'] if parsed_response['runtime'] else ""})


def add_movies_info_from_titles(movies_titles: list, target_basic_info_csv: str = None,  target_all_movies_info_csv: str = None,  target_runtime_csv: str = None,  target_simplified_credits_csv: str = None):
    correctly_named_json_paths = download_movies_tmdb_jsons_from_titles_list(movies_titles=movies_titles)
    movies_ids = get_movies_ids_from_json_paths(correctly_named_json_paths)
    save_movie_basic_info_to_csv(list_of_json_files=correctly_named_json_paths, destination_path=target_basic_info_csv)
    save_all_movie_info_to_csv(list_of_json_files=correctly_named_json_paths, destination_path=target_all_movies_info_csv)
    get_movies_runtime(movies_ids=movies_ids)
    get_movies_simplified_credits(movies_ids=movies_ids)


if __name__ == "__main__":
    # download_movies_jsons_from_tmdb_title_search(movies_csv_path=r'majstro_verko/Files/movies.csv')
    # save_movie_basic_info_to_csv(destination_path=r'majstro_verko/Files/movies_basic_info_from_tmdb.csv')
    # save_all_movie_info_to_csv()
    # try_and_correct_for_wrong_hits()
    # get_movies_simplified_credits()
    # get_movies_runtime()
    # add_movies_info_from_titles(movies_titles=[""])
    pass
    
