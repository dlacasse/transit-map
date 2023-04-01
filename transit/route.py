from dataclasses import dataclass, field
from functools import cache
from transit.stop import Stop

@dataclass
class Route:
    name: str
    id: str
    stops: list = field(default_factory=list)

    def has_stop(self, stop : Stop) -> bool:
        if stop in self.stops:
            return True
        return False

       
    def get_connections(self):
        results = []
        #print(f"Getting connections for route: {self.name}")
        for stop in self.stops:
            
            if stop.is_associated_with_multiple_routes():
                # Add a record in the results for each route -> stop combo
                for associated_route in stop.route_associations:
                    if associated_route != self.name:
                        results.append((associated_route, stop))
                        break

        return results
