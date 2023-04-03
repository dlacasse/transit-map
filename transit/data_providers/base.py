from abc import ABC, abstractmethod

class BaseDataProvider(ABC):
    @abstractmethod
    def get_all_routes(self):
        """
        Load all routes from the API
        """
        pass

    @abstractmethod
    def get_stops_for_route(self, route_id):
        """
        Load all stops for a given route
        """
        pass