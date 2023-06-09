from movie_app import MovieApp
from storage_json import StorageJson
from storage_csv import StorageCsv

amy = StorageCsv('movies.csv')
jack = StorageJson('movies.json')
movie_app = MovieApp(amy)
movie_app.run()
