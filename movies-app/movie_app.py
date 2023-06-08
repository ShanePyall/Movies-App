import json
from random import randint


class MovieApp:
    # Creates an app that allows user to interact with movies in a file.
    def __init__(self, storage):
        # points to a class with CRUD and a file path in classes self.
        self._storage = storage

    def choice_filter(self, num):
        # Filters and calls on functions associated to suer input.

        if num == "0":
            res = 0
        elif num == "1":
            res = self._command_list_movies()
        elif num == "2":
            res = self._command_add_movies()
        elif num == "3":
            res = self._command_delete_movies()
        elif num == "4":
            res = self._command_update_movies()
        elif num == "5":
            res = self._command_stats()
        elif num == "6":
            res = self._command_random_movie()
        elif num == "7":
            res = self._command_search_movie()
        elif num == "8":
            res = self._command_movies_sorted_by_rating()
        elif num == "9":
            res = self._command_generate_site()
        else:
            res = "Invalid choice"
        return res

    def _command_list_movies(self):
        # Returns a string with the list of movies
        movies = self._storage.list_movies()
        return movies

    def _command_add_movies(self):
        # Adds a new movie to data-base.
        title = input("Enter new movie name: ")
        title.replace(" ", "+")
        return self._storage.add_movie(title)

    def _command_delete_movies(self):
        # Removes movie from database
        title = input("Enter movie name to delete: ")
        return self._storage.delete_movie(title)

    def _command_update_movies(self):
        # Updates a movies information if the movie is in the database
        title = input("Enter the name of the movie you would like to comment on: ")
        note = input("Enter your comment: ")

        return self._storage.update_movie(title, note)

    def _command_stats(self):
        # Calculates and Displays stats of all movies.
        my_list = []
        temp_list = []

        with open(self._storage.file_path, "r") as json_movie_storage:
            movies = json.loads(json_movie_storage.read())

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

    def _command_random_movie(self):
        # Selects a random movie from list, using randint.
        with open(self._storage.file_path, "r") as json_movies_storage:
            movies = json.loads(json_movies_storage.read())

        movie = movies[randint(0, len(movies) - 1)]
        message = f"\nYour movie for tonight is: {movie['Title']}, it\'s rated {movie['Rating']}"
        return message

    def _command_search_movie(self):
        # Finds movie user searched for (if in data-base).
        search_input = input("\nEnter part of a movies name: ")
        message = "Movie was not found in our list, why not add it!"

        with open(self._storage.file_path, "r") as json_movie_storage:
            movies = json.loads(json_movie_storage.read())

        for movie in movies:
            if search_input in movie['Title']:  # Allows for capitalisation errors
                message = f"{movie['Title']}: {movie['Rating']}\n"

        return message

    def _command_movies_sorted_by_rating(self):
        # Stores movie ratings and keys into list, sorts by highest.

        with open(self._storage.file_path, "r") as json_movie_storage:
            movies = json.loads(json_movie_storage.read())

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

    def _command_generate_site(self):
        # Generates html movie website
        with open("bones/index_template.html", "r") as readable:
            html_code_string = readable.read()

        with open("bones/style.css", "r") as readable:
            style_sheet = readable.read()

        with open("bones/style.css", "w") as writable:
            writable.write(style_sheet)

        with open(self._storage.file_path, "r") as readable:
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

    def run(self):
        # Runs the program until user enters 0 or force stopped
        # Print menu
        print("[#][#][#][#] My Movies Database [#][#][#][#]")
        count = 0
        while count == 0:
            print("\n   ---Menu---")
            print('''0. Exit
1. List movies 
2. Add movies 
3. Delete movies 
4. Update movies 
5. Stats 
6. Random movies 
7. Search movies
8. Movies sorted by rating
9. Generate website\n''')

            # Get use command
            choice = input("Enter choice (0-9): ")
            # Execute command
            temp = self.choice_filter(choice)

            # Tuple unpacking
            if temp == 0:
                print("\nBye!\n")
                break
            else:
                print(temp)
            input("\nPress enter to continue")
