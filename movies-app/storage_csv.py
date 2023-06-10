from istorage import IStorage
from random import randint
import pandas as pd
import csv
import requests

API_KEY = 'be04b8e5'
DATA_LINK = f"http://www.omdbapi.com/?apikey={API_KEY}&t="


class StorageCsv(IStorage):
    # Stores movies CRUD data in a CSV file.
    # Requires CSV file to be formatted: Title, Rating, Year, Poser URL, Note.
    def __init__(self, file_path):
        self.file_path = file_path

    def list_movies(self):
        # Returns a string of all movies in database.

        draft = pd.read_csv(self.file_path, encoding='unicode_escape', nrows=None)
        movies = pd.DataFrame(draft)
        message = ''
        count = 0
        for index, rows in movies.iterrows():
            message += f"\n{rows[0]}: {rows[1]}, {rows[2]}"
            count += 1

        final = f"\n{count} movies in total\n" + message
        return final

    def add_movie(self, title, note=''):
        # Adds user input (title) to search link and prints(for now) the expected.
        res = requests.get(DATA_LINK + title)
        parsed = res.json()
        if parsed["Response"] == "False":
            message = f"\nSorry, we couldn't find {title} anywhere. Please double check your spelling"
            return message
        new_movie_dict = {"Title": parsed["Title"], "Rating": parsed["Ratings"][0]["Value"], "Year": parsed["Year"],
                          "Poster URL": parsed["Poster"], "Note": note}

        movies = pd.read_csv(self.file_path, encoding='unicode_escape', nrows=None)
        for index, row in movies.iterrows():
            if row[0] == parsed['Title']:
                return f'Movie {parsed["Title"]} is already in our list'

        with open(self.file_path, 'a') as writable:
            fieldnames = ["Title", "Rating", "Year", "Poster URL", "Note"]
            writer = csv.DictWriter(writable, fieldnames=fieldnames)
            writer.writerow(new_movie_dict)

        message = f'Movie {parsed["Title"]} successfully added!'
        return message

    def delete_movie(self, title):
        # Delete movie from database(If it exists/is valid)
        movies = pd.read_csv(self.file_path, encoding='unicode_escape', nrows=None)
        message = f"Movie {title} does not exist (In our database at-least)!"  # If movie title not in dict

        for index, row in movies.iterrows():
            if row[0] == title:
                movies = movies.drop(index=index)  # Removes movie from file
                message = f"Movie {title} successfully deleted"

        movies.to_csv(self.file_path, index=False)
        return message

    def update_movie(self, title, note):
        # Updates movies: if present in list, and if data is valid.
        movies = pd.read_csv(self.file_path, encoding='unicode_escape', nrows=None)
        message = f'''Unfortunately we could not find "{title}" in our data base.
Please double check your spelling or maybe expand our list!'''

        for index, row in movies.iterrows():
            if row[0] == title:
                row[-1] = note
                movies.to_csv(self.file_path, index=False)
                message = f"Your note has been added to the movie!"
                break

        return message

    def command_stats(self):
        # Calculates and Displays stats of all movies.
        my_list = []
        temp_list = []

        movies = pd.read_csv(self.file_path, encoding='unicode_escape', nrows=None)

        for index, movie in movies.iterrows():
            temp_list.append(movie[1])

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
        for index, movie in movies.iterrows():
            if movie[1][:3] == str(list2[-1]):
                best_movie = movie[0]
            if movie[1][:3] == str(list2[0]):
                worst_movie = movie[0]

        # Store results in message
        message = f'''\nAverage rating: {round(average_rating, 1)}
Median rating: {my_list[middle_of_list]}
Best movie: {best_movie}, {list2[-1]}
Worst movie: {worst_movie}, {list2[0]}'''

        return message

    def command_random_movie(self):
        # Selects a random movie from list, using randint.
        movies = pd.read_csv(self.file_path, encoding='unicode_escape', nrows=None)
        movie_list = []
        for index, movie in movies.iterrows():
            movie_list.append(movie)
        movie = movie_list[randint(0, len(movie_list) - 1)]
        message = f"\nYour movie for tonight is: {movie[0]}, it\'s rated {movie[1]}"
        return message

    def command_search_movie(self, search_input):
        # Finds movie user searched for (if in data-base).
        message = ''
        movies = pd.read_csv(self.file_path, encoding='unicode_escape', nrows=None)

        checker = False
        for index, movie in movies.iterrows():
            if search_input in movie[0]:  # Allows for capitalisation errors
                checker = True
                message += f"\n{movie[0]}: {movie[1]}"

        if checker is False:
            message = "Movie was not found in our list, why not add it!\n"

        return message

    def command_movies_sorted_by_rating(self):
        # Stores movie ratings and keys into list, sorts by highest.
        movies = pd.read_csv(self.file_path, encoding='unicode_escape', nrows=None)
        temp_list = []
        value_list = []

        for index, movie in movies.iterrows():
            temp_list.append(movie[1])

        for items in temp_list:
            if '/' in str(items):
                items = float(items.split('/')[0])
            value_list.append(items)

        value_list.sort(reverse=True)

        key_list = []
        for item in value_list:
            for index, movie in movies.iterrows():
                if '/' in str(movie[1]):
                    target = str(movie[1])[:3]
                else:
                    target = movie[1]

                if float(target) == item:
                    key_list.append(movie[0])

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

        with open("bones/style.css", "w") as writable:
            writable.write(style_sheet)

        movies = pd.read_csv(self.file_path, encoding='unicode_escape', nrows=None)
        res = ''
        img_link = None

        for index, movie in movies.iterrows():
            try:
                img_link = movie[3]

            except KeyError:
                img_link = """https://d32qys9a6wm9no.cloudfront.net/images\
    /others/not_available/poster_500x735.png?t=1683418449"""

            finally:
                movie_title = movie[0]
                movie_year = movie[2]
                # movie_rating = movie[1]
                if movie[4] is not None:
                    movie_note = movie[4]
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
