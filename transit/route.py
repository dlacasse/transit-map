from dataclasses import dataclass, field
from functools import cache
from transit.stop import Stop

@dataclass
class Route:
    name: str
    id: str
    stops: list = field(default_factory=list)
    line_name: str = field(default=None)


    def has_stop(self, stop : Stop) -> bool:
        """
        Check if this route contains the provided stop
        """
        if stop in self.stops:
            return True
        return False
    

    def has_stops(self, stop1, stop2):
        """
        Check if this route contains both stops (we could probably make this accept *args)
        """
        return self.has_stop(stop1) and self.has_stop(stop2)
       

    def get_connecting_stops(self):
        """
        Return a list of stops for this route which are associated with multiple routes
        """
        results = []
        for stop in self.stops:
            if stop.is_associated_with_multiple_routes():
                results.append(stop)
        return results


    def get_connecting_routes(self):
        """
        Look through the list of stops to find all routes that are adjacent
        """
        results = []

        for stop in self.stops:
            if stop.is_associated_with_multiple_routes():
                for associated_route in stop.route_associations:
                    if associated_route not in results and associated_route != self.name:
                        results.append(associated_route)

        return results
