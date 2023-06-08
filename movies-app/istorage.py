from abc import ABC, abstractmethod


class IStorage(ABC):
    # Interface that shows all 4 CRUD commands available
    @abstractmethod
    def list_movies(self):
        pass

    @abstractmethod
    def add_movie(self, title):
        pass

    @abstractmethod
    def delete_movie(self, title):
        pass

    @abstractmethod
    def update_movie(self, title, notes):
        pass
