from functools import cache
from transit.stop import Stop
from transit.route import Route


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
            self.load_routes()
        
        for route_name in self.routes.keys():
            route = self.routes[route_name]
            stops = self.data_provider.get_stops_for_route(route.id)
           
            for stop in stops:
                # Add this to the list of all stops if we haven't already seen it
                if stop.name not in self.stops:
                    stop.route_associations.append(route.name)
                    self.stops[stop.name] = stop
                else:
                    # Otherwise, just append the list of routes
                    self.stops[stop.name].route_associations.append(route.name)
                
                # Add this stop to the route info
                route.stops.append(self.stops[stop.name])
                    

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


    @cache
    def __get_route_stats(self):
        """
        Helper function which returns a list of tuples (route name, count stops)
        """
        stop_counts = [(name, len(details.stops)) for name, details in self.routes.items()]
        return sorted(stop_counts, key=lambda stop: stop[1])


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


    def get_stop_from_string(self, stop_string) -> Stop:
        if stop_string in self.stops:
            return self.stops[stop_string]
        else:
            raise Exception('Unknown Stop!')


    def get_route_from_string(self, route_string) -> Route:
        if route_string in self.routes:
            return self.routes[route_string]
        else:
            raise Exception('Unknown Route!')
    

    def get_routes_for_stops(self, origin: Stop, destination: Stop, checked_routes = None) -> list:
        """
        Try to determine a list of routes between stops (can result in recursive calls)
        """
        results = []

        if checked_routes is None:
            checked_routes = []

        # Attempt to short-circuit the logic below by looking for any direct routes
        # This may seem a bit redundant, but as a base case, we want to exhaust all potential direct routes 
        # before searching connections or possibly recursing
        for route_string in origin.route_associations:
            route = self.get_route_from_string(route_string)

            if route.has_stops(origin, destination):
                results.append(route_string)
                return results
           
        # Check all of the routes associated with the origin
        for route_string in origin.route_associations:
            if route_string in checked_routes:
                continue
            
            # Keep track of what's already been checked
            checked_routes.append(route_string)
            route = self.get_route_from_string(route_string)

            # If we didn't find a direct connection on this route, start looking for "intersecting routes"
            for connecting_route in route.get_connecting_routes():
                if connecting_route in destination.route_associations:
                    return [route_string, connecting_route]

            # If all else fails, we need to look through connecting stops
            for intersection_stop in route.get_connecting_stops():
                result = self.get_routes_for_stops(intersection_stop, destination, checked_routes)
                
                if result:
                    results.append(route_string)
                    results.extend(result)
                    return results
    
        return []
