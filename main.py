from functools import cache
import requests

# --------
from dataclasses import dataclass, field

@dataclass
class Route:
    name: str
    id: str
    stops: list = field(default_factory=list)

@dataclass
class Stop:
    name: str
    route_associations: list = field(default_factory=list)

# --------

class DataProvider():
    pass

class MBTADataProvider():
    API_BASE_URL = "https://api-v3.mbta.com/"

    def get_all_routes(self):
        method_route = "routes?filter[type]=0,1"       
        route_list = self.get_api_results(method_route)

        routes = []
        for route in route_list:
            route_details = route['attributes']
            route_name = route_details['long_name']
        
            routes.append(Route(
                name=route_name,
                id=route['id']
            ))

        return routes


    def get_stops_for_route(self, route_id):
        method_route = f"stops?filter[route]={route_id}"
        stop_list = self.get_api_results(method_route)
     
        stops = []
        for stop in stop_list:
            stop_attributes = stop['attributes']
            stop_name = stop_attributes['name']

            stops.append(Stop(
                name=stop_name
            ))
            
        return stops
    

    def get_api_results(self, endpoint):
        url = self.API_BASE_URL + endpoint
        
        response = requests.get(url)

        if response.status_code == 200:
            return response.json()['data']
        else:
            raise Exception(f"API Unavailable - Status code: {response.status_code}")



class TransitMap():
    routes = {}
    stops = {}
    data_provider = None
    
    def __init__(self, data_provider=None) -> None:
        self.data_provider = data_provider

    @cache
    def load_routes(self):       
        route_list = self.data_provider.get_all_routes()

        for route in route_list:
            self.routes[route.name] = route
            
    @cache
    def load_stops(self):
        if not self.routes:
            raise Exception('No stops loaded')
        
        for route_name in self.routes.keys():
            route = self.routes[route_name]
            stops = self.data_provider.get_stops_for_route(route.id)
           
            for stop in stops:
                # Add this stop to the route info
                route.stops.append(stop.name)

                # Add this to the list of all stops if we haven't already seen it
                if stop.name not in self.stops:
                    stop.route_associations.append(route_name)
                    self.stops[stop.name] = stop
                else:
                    # Otherwise, just append the list of routes
                    self.stops[stop.name].route_associations.append(route_name)


    @cache
    def __get_route_stats(self):
        """
        Helper function which returns a list of tuples (route name, count stops)
        """
        stop_counts = [(name, len(details.stops)) for name, details in self.routes.items()]
        return sorted(stop_counts, key=lambda stop: stop[1])


    @cache
    def get_connecting_stops(self):
        """
        We'll define "connecting stops" as stops that service two or more routes
        """
        connecting_stops = {}
        for stop_name, stop_details in self.stops.items():
            if len(stop_details.route_associations) >= 2:
                connecting_stops[stop_name] = stop_details.route_associations
        return connecting_stops


    def get_routes_with_most_stops(self):
        # TODO: fix this
        # There can be ties, so we may return multiples
        stop_list = []
        max_value = None
        route_stats = self.__get_route_stats()
        
        for x in range(len(route_stats)-1, 0, -1):
            if max_value is None:
                max_value = route_stats[x][1]
                stop_list.append(route_stats[x])
                continue

            if route_stats[x][1] >= max_value:
                stop_list.append(route_stats[x])
            else:
                break

        return stop_list
    
    def get_routes_with_least_stops(self):
        # TODO: fix this
        return [self.__get_route_stats()[0]]
       


class CLI():
    transit_map = None

    def __init__(self) -> None:
        mbta_data_provider = MBTADataProvider()
        self.transit_map = TransitMap(mbta_data_provider)

    def display_all_routes(self):
        self.transit_map.load_routes()
        print("\nAll Subway routes: ", self.get_divider())

        # Assumption: We should sort these so they are in a consistent order
        for route_name in sorted(self.transit_map.routes.keys()):
            print(route_name)

    def get_divider(self):
        return "\n" + ("=" * 30)

    def display_stop_statistics(self):
        """
        1. The name of the subway route with the most stops as well as a count of its stops.
        2. The name of the subway route with the fewest stops as well as a count of its stops.
        3. A list of the stops that connect two or more subway routes along with the relevant route names for
        each of those stops.
        """
        self.transit_map.load_routes()
        self.transit_map.load_stops()
        
        print("\nThe subway route(s) with the most stops are: ", self.get_divider())
        
        for name, count in self.transit_map.get_routes_with_most_stops():
            print(f"{name}: {count}")
        
        print("\nThe subway route(s) with the fewest stops are: ", self.get_divider())
        for name, count in self.transit_map.get_routes_with_least_stops():
            print(f"{name}: {count}")

        print("\nSubway stops that connect two or more routes: ", self.get_divider())
        connecting_stops = self.transit_map.get_connecting_stops()
        for stop_name, connecting_routes in sorted(connecting_stops.items()):
            print(f"{stop_name} ({', '.join(sorted(connecting_routes))})")

      
"""
    Entrypoint to run when the script is directly invoked.
"""
if __name__ == "__main__":
    transit_cli = CLI()

    # Question 1
    transit_cli.display_all_routes()


    # Question 2
    transit_cli.display_stop_statistics()

    