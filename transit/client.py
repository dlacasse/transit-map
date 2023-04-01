from transit.data_providers.mbta import MBTADataProvider
from transit.system import TransitMap
from transit.stop import Stop

class CLI():
    transit_map = None

    def __init__(self) -> None:
        mbta_data_provider = MBTADataProvider()
        self.transit_map = TransitMap(mbta_data_provider)


    def get_divider(self):
        return "\n" + ("=" * 30)

    
    def display_all_routes(self):
        self.transit_map.load_routes()
        print("\nAll Subway routes: ", self.get_divider())

        # Assumption: We should sort these so they are in a consistent order
        for route_name in sorted(self.transit_map.routes.keys()):
            print(route_name)


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


    def display_travel_route_prompt(self):
        """
        Displays the prompt which asks users to enter their origin, destination
        """
        while True:
            origin = input("Enter origin: ")
            destination = input("Enter destination: ")

            if 'exit' in [origin.lower(), destination.lower()]:
                break
            
            self.get_travel_info(origin, destination)


    def get_travel_info(self, origin_string, destination_string):      
        print(f"\n{origin_string} -> {destination_string}", self.get_divider())
        
        # TODO: Error handling for missing
        origin = self.transit_map.stops[origin_string]
        destination = self.transit_map.stops[destination_string]
        
        print("\nFinal Result: ", self.transit_map.get_routes_for_stops(origin,destination))
