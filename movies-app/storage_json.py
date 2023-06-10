from istorage import IStorage
from random import randint
import json
import requests

API_KEY = 'be04b8e5'
DATA_LINK = f"http://www.omdbapi.com/?apikey={API_KEY}&t="


class StorageJson(IStorage):
    # Stores movies CRUD data in a Json file.
    def __init__(self, file_path):
        self.file_path = file_path

    def list_movies(self):
        # Returns a string of all movies in database.
        with open(self.file_path, "r") as json_movie_storage:
            movies = json.loads(json_movie_storage.read())

        list_of_movies_text = f"\n{len(movies)} movies in total\n"
    
        for movie in movies:
            list_of_movies_text += f"\n{movie['Title']}: {movie['Rating']}, {movie['Year']}"

        return list_of_movies_text

    def add_movie(self, title, note):
        # Adds user input (title) to search link and prints(for now) the expected.
        res = requests.get(DATA_LINK + title)
        parsed = res.json()
        if parsed["Response"] == "False":
            message = f"\nSorry, we couldn't find {title} anywhere. Please double check your spelling"
            return message

        with open(self.file_path, "r") as readable:
            movies = json.loads(readable.read())

        new_movie_dict = {"Title": parsed["Title"], "Rating": parsed["Ratings"][0]["Value"], "Year": parsed["Year"],
                          "Poster URL": parsed["Poster"], "Note": note}

        for movie in movies:
            if movie["Title"] == new_movie_dict["Title"]:
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

    def command_stats(self):
        # Calculates and Displays stats of all movies.
        my_list = []
        temp_list = []

        with open(self.file_path, "r") as readable:
            movies = json.loads(readable.read())

        for movie in movies:
            temp_list.append(movie['Rating'])

        for items in temp_list:
            if '/' in str(items):
                items = float(items.split('/')[0])
            my_list.append(items)

        list2 = my_list.copy()  # Need to make a copy so median of list is accurate.
        list2.sort()  # Needed to calculate best and worst

        # Average solving and assigning
        my_sum = 0
        for item in my_list:
            my_sum += item
        average_rating = my_sum / len(my_list)

        # Prep to work out the median
        if len(my_list) % 2 == 0:
            middle_of_list = int((len(my_list) / 2) - 1)
        else:
            middle_of_list = int((len(my_list) - 1) / 2)

        # Get best and worst movie
        best_movie = None
        worst_movie = None
        for movie in movies:
            if movie["Rating"][:3] == str(list2[-1]):
                best_movie = movie["Title"]
            if movie["Rating"][:3] == str(list2[0]):
                worst_movie = movie["Title"]

        # Store results in message
        message = f'''\nAverage rating: {round(average_rating, 1)}
Median rating: {my_list[middle_of_list]}
Best movie: {best_movie}, {list2[-1]}
Worst movie: {worst_movie}, {list2[0]}'''

        return message

    def command_random_movie(self):
        # Selects a random movie from list, using randint.
        with open(self.file_path, "r") as readable:
            movies = json.loads(readable.read())

        movie = movies[randint(0, len(movies) - 1)]
        message = f"\nYour movie for tonight is: {movie['Title']}, it\'s rated {movie['Rating']}"
        return message

    def command_search_movie(self, search_input):
        # Finds movie user searched for (if in data-base).
        message = ''

        with open(self.file_path, "r") as readable:
            movies = json.loads(readable.read())

        checker = False
        for movie in movies:
            if search_input in movie['Title']:  # Allows for capitalisation errors
                checker = True
                message += f"\n{movie['Title']}: {movie['Rating']}"

        if checker is False:
            message = "\nMovie was not found in our list, why not add it!"

        return message

    def command_movies_sorted_by_rating(self):
        # Stores movie ratings and keys into list, sorts by highest.

        with open(self.file_path, "r") as readable:
            movies = json.loads(readable.read())

        temp_list = []
        value_list = []
        for movie in movies:
            temp_list.append(movie['Rating'])

        for items in temp_list:
            if '/' in str(items):
                items = float(items.split('/')[0])
            value_list.append(items)

        value_list.sort(reverse=True)

        key_list = []
        for item in value_list:
            for movie in movies:
                if '/' in str(movie['Rating']):
                    target = str(movie['Rating'])[:3]
                else:
                    target = movie['Rating']

                if float(target) == item:
                    key_list.append(movie['Title'])

        key_list = list(dict.fromkeys(key_list))
        message = ''
        for num in range(len(key_list)):
            message += f"\n{key_list[num]}: {value_list[num]}"

        return message

    def command_generate_site(self):
        # Generates html movie website
        with open("bones/index_template.html", "r") as readable:
            html_code_string = readable.read()

        with open("bones/style.css", "r") as readable:
            style_sheet = readable.read()

        with open("style.css", "w") as writable:
            writable.write(style_sheet)

        with open(self.file_path, "r") as readable:
            movies = json.loads(readable.read())

        res = ''
        img_link = None
        for movie in movies:

            try:
                img_link = movie["Poster URL"]

            except KeyError:
                img_link = """https://d32qys9a6wm9no.cloudfront.net/images\
        /others/not_available/poster_500x735.png?t=1683418449"""

            finally:
                movie_title = movie["Title"]
                movie_year = movie["Year"]
                # movie_rating = movie["Rating"]
                if "Note" in movie:
                    movie_note = movie["Note"]
                else:
                    movie_note = ''

                start = f'<li><div class="movie" >'

                img_text = f'<img class="movie-poster" src="{img_link}" title="{movie_note}"/>'
                title_text = f'<div class="movie-title">{movie_title}</div>'
                year_text = f'<div class="movie-year">{movie_year}</div>'

                end = f'</div></li><br>'
                res += start + img_text + title_text + year_text + end

        result = html_code_string.replace("__TEMPLATE_TITLE__", "Mock-Buster!")
        final = result.replace("__TEMPLATE_MOVIE_GRID__", res)

        with open("movie_web_app.html", "w") as website_maker:
            website_maker.write(final)

        message = "Website was generated successfully!"
        return message
