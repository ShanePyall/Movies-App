from istorage import IStorage
import json
import requests

API_KEY = 'be04b8e5'
DATA_LINK = f"http://www.omdbapi.com/?apikey={API_KEY}&t="


class StorageJson(IStorage):
    # Defines location for objects file to read and write from
    def __init__(self, file_path):
        self.file_path = file_path

    def list_movies(self):
        # Returns a string of all movies in database.
        with open(self.file_path, "r") as json_movie_storage:
            movies = json.loads(json_movie_storage.read())

        list_of_movies_text = f"\n{len(movies)} movies in total\n"
    
        for movie in movies:
            list_of_movies_text += f"\n{movie['Title']}: {movie['Rating']}, {movie['Year']}"

        list_of_movies_text += "\n"
        return list_of_movies_text

    def add_movie(self, title):
        # Adds user input (title) to search link and prints(for now) the expected.
        res = requests.get(DATA_LINK + title)
        parsed = res.json()

        with open(self.file_path, "r") as readable:
            movies = json.loads(readable.read())

        new_movie_dict = {"Title": parsed["Title"], "Rating": parsed["Ratings"][0]["Value"], "Year": parsed["Year"],
                          "Poster URL": parsed["Poster"]}

        for movie in movies:
            if movie["Title"] == new_movie_dict["Title"]:
                print(True)
                return f'Movie {new_movie_dict["Title"]} is already in our list'
        movies.append(new_movie_dict)

        with open(self.file_path, "w") as writable:
            writable.write(json.dumps(movies))

        message = f'Movie {new_movie_dict["Title"]} successfully added!'
        return message

    def delete_movie(self, title):
        # Delete movie from database(If it exists/is valid)
        with open(self.file_path, "r") as json_movie_storage:
            movies = json.loads(json_movie_storage.read())

        message = f"Movie {title} does not exist (In our database at-least)!"  # If movie title not in dict

        for movie in movies:
            if movie["Title"] == title:
                movies.remove(movie)  # Removes movie from list
                message = f"Movie {title} successfully deleted"

        with open(self.file_path, "w") as json_movie_storage:
            json_movie_storage.write(json.dumps(movies))

        return message

    def update_movie(self, title, note):
        # Updates movies: if present in list, and if data is valid.
        with open(self.file_path, "r") as readable:
            movies = json.loads(readable.read())

        count = 0
        index = -1

        for movie in movies:
            if movie['Title'] == title:
                index = movies.index(movie)
                count += 1
            if count > 0:
                break

        if count == 0:
            return f'''Unfortunately "{title}" is not in our data base.
        Double check your spelling or maybe expand our list!'''

        movies[index]['Note'] = note
        message = f"Your note has been added to the movie!"

        with open(self.file_path, "w") as writable:
            writable.write(json.dumps(movies))

        return message
