
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
        note = input("Would you like to leave a comment about this movie(If not, please leave empty): ")
        title.replace(" ", "+")
        return self._storage.add_movie(title, note)

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
        return self._storage.command_stats()

    def _command_random_movie(self):
        # Selects a random movie from list, using randint.
        return self._storage.command_random_movie()

    def _command_search_movie(self):
        # Finds movie user searched for (if in data-base).
        search_input = input("\nEnter part of a movies name: ")
        return self._storage.command_search_movie(search_input)

    def _command_movies_sorted_by_rating(self):
        # Stores movie ratings and keys into list, sorts by highest.
        return self._storage.command_movies_sorted_by_rating()

    def _command_generate_site(self):
        # Generates html movie website
        return self._storage.command_generate_site()

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
