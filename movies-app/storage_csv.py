from istorage import IStorage
import csv
import requests

API_KEY = 'be04b8e5'
DATA_LINK = f"http://www.omdbapi.com/?apikey={API_KEY}&t="


class StorageCsv(IStorage):
    # Stores movies CRUD data in a CSV file.
    def __init__(self, file_path):
        self.file_path = file_path

    def list_movies(self):
        # Returns a string of all movies in database.
        with open(self.file_path, "r") as csv_movie_storage:
            movies = csv.reader(csv_movie_storage)

        count = 0
        list_of_movies_text = ''
        for row in movies:
            if count == 0:
                continue
            list_of_movies_text += f"\n{row['Title']}: {row['Rating']}, {row['Year']}"
            count += 1
        final = f"\n{count} movies in total\n" + list_of_movies_text

        final += "\n"
        return final

    def add_movie(self, title):
        # Adds user input (title) to search link and prints(for now) the expected.
        res = requests.get(DATA_LINK + title)
        parsed = res.json()

        with open(self.file_path, "r") as readable:
            movies = csv.reader(readable)

        new_movie_dict = {"Title": parsed["Title"], "Rating": parsed["Ratings"][0]["Value"], "Year": parsed["Year"],
                          "Poster URL": parsed["Poster"]}

        for movie in movies:
            if movie["Title"] == new_movie_dict["Title"]:
                return f'Movie {new_movie_dict["Title"]} is already in our list'

        with open(self.file_path, "w") as writable:
            fieldnames = ["Title", "Rating", "Year", "Poster URL", "Note"]
            writer = csv.DictWriter(writable, fieldnames=fieldnames)

            writer.writeheader()
            writer.writerow(new_movie_dict)

        message = f'Movie {new_movie_dict["Title"]} successfully added!'
        return message

    def delete_movie(self, title):
        # Delete movie from database(If it exists/is valid)
        with open(self.file_path, "r") as readable:
            movies = csv.reader(readable)

        message = f"Movie {title} does not exist (In our database at-least)!"  # If movie title not in dict

        for movie in movies:
            if movie['Title'] == title:
                movies = movies.drop(movies[movies.movie].index)  # Removes movie from file
                message = f"Movie {title} successfully deleted"

        with open(self.file_path, "w") as writable:
            fieldnames = ["Title", "Rating", "Year", "Poster URL", "Note"]
            writer = csv.DictWriter(writable, fieldnames=fieldnames)
            writer.writer(movies)

        return message

    def update_movie(self, title, note):
        # Updates movies: if present in list, and if data is valid.
        with open(self.file_path, "r") as readable:
            movies = csv.reader(readable)

        count = 0

        row = None
        for movie in movies:
            if movie['Title'] == title:
                row = movie
                count += 1
            if count > 0:
                break

        if count == 0:
            return f'''Unfortunately "{title}" is not in our data base.
        Double check your spelling or maybe expand our list!'''

        if row is not None:
            row['Note'] = note
            message = f"Your note has been added to the movie!"

            with open(self.file_path, "w") as writable:
                fieldnames = ["Title", "Rating", "Year", "Poster URL", "Note"]
                writer = csv.DictWriter(writable, fieldnames=fieldnames)
                writer.writer(movies)

        else:
            message = """We had an issue locating your movie,\
                       Please ensure the movie is present in our list and its spelling is correct"""

        return message
