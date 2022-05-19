from pathlib import Path
import csv
import requests
import json

def get_movie_titles_from_csv(movies_csv_path: str = None) -> list:
    if movies_csv_path is None:
        movies_csv_path = r'majstro_verko/Files/movies.csv'
    with open(movies_csv_path, newline='\n', mode='r', encoding='utf-8-sig') as csv_file:
        reader = csv.DictReader(csv_file, delimiter=',', dialect='unix')
        list_of_movies_titles = [row['title'] for row in reader if row['title'] != '' ]
    return list_of_movies_titles

def download_movies_jsons_from_tmdb_title_search(movies_csv_path: str = None, api_keys_path: str = None):
    headers = {'Accept': 'application/json'}
    if movies_csv_path is None:
        movies_csv_path = r'majstro_verko/Files/movies.csv'
    if api_keys_path is None:
        api_key = Path(r'API_keys/TMDB_API_Key.txt').read_text().strip()
    list_of_movies_titles = get_movie_titles_from_csv()
    for movie_title in list_of_movies_titles:
        api_url = f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&language=en-US&query={movie_title}&page=1&include_adult=false"
        response = requests.get(api_url, headers=headers)
        with open(f'majstro_verko/Files/Movies_jsons/{movie_title}.json', 'wb') as outf:
            outf.write(response.content)

def parse_json_from_list_of_files(json_names_with_path: list = None) -> list:
    if json_names_with_path is None:
        list_of_movies_titles = get_movie_titles_from_csv()
        json_names_with_path = [f'majstro_verko/Files/Movies_jsons/{movie_title}.json' for movie_title in list_of_movies_titles]
    parsed_json = [json.load(Path(json_path).open()) for json_path in json_names_with_path]
    return parsed_json

if __name__ == "__main__":
    parsed = parse_json_from_list_of_files()
    movies_basic_info = [{'title': movie['results'][0]['title'], 'original_title': movie['results'][0]['original_title'], 'year': movie['results'][0]['release_date'][:4]} for movie in parsed if movie['results']]
    with open(r'majstro_verko/Files/movies_basic_info_from_tmdb.csv', 'w') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=["title", "original_title", "year"], dialect="unix")
        writer.writeheader()
        for movie in movies_basic_info:
            writer.writerow(movie)



