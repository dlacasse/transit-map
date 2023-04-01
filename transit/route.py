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
        if stop in self.stops:
            return True
        return False
    
    def has_stops(self, stop1, stop2):
        return self.has_stop(stop1) and self.has_stop(stop2)
       
    def get_connecting_stops(self):
        results = []
        for stop in self.stops:
            if stop.is_associated_with_multiple_routes():
                for associated_route in stop.route_associations:
                    if associated_route != self.name:
                        results.append(stop)
                        break

        return results

    def get_connecting_routes(self):
        results = []

        for stop in self.stops:
            if stop.is_associated_with_multiple_routes():
                for associated_route in stop.route_associations:
                    if associated_route not in results and associated_route != self.name:
                        results.append(associated_route)
        return results
    
    def part_of_same_line(self, route_to_compare):
        if self.line_name == route_to_compare.line_name:
            return True
        else:
            return False
