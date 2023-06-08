from movie_app import MovieApp
from storage_json import StorageJson

amy = StorageJson('movies.json')
jack = StorageJson('movies.json')
movie_app = MovieApp(amy)
movie_app.run()
