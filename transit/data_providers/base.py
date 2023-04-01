from abc import ABC, abstractmethod

class BaseDataProvider(ABC):
    @abstractmethod
    def get_all_routes(self):
        pass

    @abstractmethod
    def get_stops_for_route(self, route_id):
        pass