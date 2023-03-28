from functools import cache
import requests

class DataProvider():
    pass

class MBTADataProvider():
    pass

class Route:
    pass

class Stop:
    pass


class TransitMap():
    routes = {}
    stops = {}
    data_provider = None
    
    def __init__(self, data_provider=None) -> None:
        pass
    

    def load_routes(self):
        # We don't need to load this again
        if self.routes:
            return
        
        route_list = self.__get_all_routes()

        for route in route_list:
            route_details = route['attributes']
            route_name = route_details['long_name']
            self.routes[route_name] = route_details
            self.routes[route_name]["id"] = route['id']
            self.routes[route_name]["stops"] = []
            

    def load_stops(self):
        if not self.routes:
            raise Exception('No stops loaded')
        
        for route_name, route_details in self.routes.items():
            stop_list = self.__get_stops_for_route(route_details['id'])

            for stop in stop_list:
                stop_attributes = stop['attributes']
                stop_name = stop_attributes['name']
                
                # Add this stop to the route info
                self.routes[route_name]["stops"].append(stop_name)

                # Add this stop if we haven't already seen it
                if stop_name not in self.stops:
                    stop_attributes['route_associations'] = [route_name]
                    self.stops[stop_name] = stop_attributes
                else:
                    self.stops[stop_name]['route_associations'].append(route_name)         


    def __get_all_routes(self):
        # TODO: Error handling
        URL = "https://api-v3.mbta.com/routes?filter[type]=0,1"
        response = requests.get(URL)
        #if response.status_code == 200:
        return response.json()['data']


    def __get_stops_for_route(self, route_id):
        URL = f"https://api-v3.mbta.com/stops?filter[route]={route_id}"
        response = requests.get(URL)
        return response.json()['data']

    @cache
    def __get_route_stats(self):
        stop_counts = [(name, len(details["stops"])) for name, details in self.routes.items()]
        return sorted(stop_counts, key=lambda stop: stop[1])


    @cache
    def get_connecting_stops(self):
        """
        We'll define "connecting stops" as stops that service two or more routes
        """
        connecting_stops = {}
        for stop_name, stop_details in self.stops.items():
            if len(stop_details['route_associations']) >= 2:
                connecting_stops[stop_name] = stop_details['route_associations']
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
        self.transit_map = TransitMap()

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

    