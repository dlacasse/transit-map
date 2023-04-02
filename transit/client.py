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
        """
        Prints a list of all current Subway routes
        """
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

        print("\nSubway stops which connect two or more routes: ", self.get_divider())
        connecting_stops = self.transit_map.get_connecting_stops()
        for stop_name, connecting_routes in sorted(connecting_stops.items()):
            print(f"{stop_name} ({', '.join(sorted(connecting_routes))})")


    def display_travel_route_prompt(self):
        """
        Displays the prompt which asks users to enter their origin, destination
        """
        while True:
            print(f"\n\nRoute Finder", self.get_divider())
            origin_string = input("Enter origin: ")

            # graceful exit
            if 'exit' == origin_string.lower():
                break

            destination_string = input("Enter destination: ")

            try:
                origin = self.transit_map.get_stop_from_string(origin_string)
                destination = self.transit_map.get_stop_from_string(destination_string)
            except:
                print(f"Unknown origin -> destination: [{origin_string}] -> [{destination_string}]")
                continue

            try:
                self.get_travel_info(origin, destination)
            except Exception as e:
                print(f"An error occurred: {e}")   
    

    def get_travel_info(self, origin : Stop, destination : Stop):
        """
        Wrapper around `get_routes_for_stops()`
        """
        print(f"\n{origin.name} to {destination.name} ->", ", ".join(self.transit_map.get_routes_for_stops(origin, destination)))
