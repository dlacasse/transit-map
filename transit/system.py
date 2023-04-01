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
    

    def get_routes_for_stops(self, origin: Stop, destination: Stop, checked = None) -> list:
        """
        Try to determine a list of routes between stops (can result in recursive calls)
        """
        results = []

        if checked is None:
            checked = []

        # Attempt to short-circuit the logic below by looking for any direct routes
        common_routes = set(origin.route_associations).intersection(set(destination.route_associations))
        if len(common_routes) > 0:
            return list(common_routes)
       
        # Check all of the routes associated with the origin
        for route_string in origin.route_associations:
            if route_string in checked:
                continue
            
            # Keep track of what's already been checked
            checked.append(route_string)

            route = self.get_route_from_string(route_string)

            # If we didn't find a direct connection on this route, start looking for "intersecting routes"
            for intersect_tpl in route.get_connections():
                intersecting_route, intersection_stop = intersect_tpl

                if intersecting_route in checked:
                    continue
                

                # If we've found a route directly in the intersection, we're done
                if intersecting_route in destination.route_associations:
                    return [route_string, intersecting_route]
                else:
                    # Otherwise, we need to recurse and keep looking
                    result = self.get_routes_for_stops(intersection_stop, destination, checked)
                    
                    if result:
                        results.append(route_string)
                        results.extend(result)
                        return results
        
        return []
    
# class OldTransitMap():
#     @cache
#     def load_routes(self):       
#         route_list = self.data_provider.get_all_routes()

#         for route in route_list:
#             self.routes[route.name] = route
            
#     @cache
#     def load_stops(self):
#         if not self.routes:
#             raise Exception('No stops loaded')
        
#         for route_name in self.routes.keys():
#             route = self.routes[route_name]
#             stops = self.data_provider.get_stops_for_route(route.id)
           
#             for stop in stops:
#                 # Add this stop to the route info
#                 route.stops.append(stop.name)

#                 # Add this to the list of all stops if we haven't already seen it
#                 if stop.name not in self.stops:
#                     stop.route_associations.add(route_name)
#                     self.stops[stop.name] = stop
#                 else:
#                     # Otherwise, just append the list of routes
#                     self.stops[stop.name].route_associations.add(route_name)

#     def get_hub_containing_routes(self, target_routes):
#         for stop, routes in self.get_connecting_stops().items():
#             if target_routes.issubset(routes):
#                 return self.stops[stop]
#         return None

#     def get_hub_services_any_route(self, starting_route, target_routes):
#         for stop, routes in self.get_connecting_stops().items():
#             if starting_route in routes and target_routes.intersection(routes):
#                 return self.stops[stop]
#         return None

#     def get_routes_for_stops(self, origin : Stop, destination: Stop):
#         routes=[]

#         direct_route = origin.route_associations.intersection(destination.route_associations)

#         if direct_route:
#             return direct_route        
    
#         for route in origin.route_associations:

#             # If the destination is a hub, we can take any route to get there (the first should do it).
#             if destination.name in self.get_connecting_stops():
#                 print('Hub target: ', destination.route_associations)
#                 hub_stop = self.get_hub_services_any_route(route, destination.route_associations)

#             else:
#                 # Otherwise, this is a regular stop and we need to make sure the hub services all 
#                 # associated routes
#                 target_routes = set([route]).union(destination.route_associations)
#                 hub_stop = self.get_hub_containing_routes(target_routes)
            
#             if hub_stop is not None:
#                 print("Found a hub that services these routes! ", hub_stop)
#                 # Add the route for origin -> hub
#                 routes.append(route)

#                 # Find and add the route for hub -> destination
#                 routes.append(self.get_routes_for_stops(hub_stop, destination))
                
#                 break
            
#         # If we still don't have a route, we need to keep trying
#         if not routes:
#             for stop, connecting_routes in self.get_connecting_stops().items():
           
#                 # Look for connecting stops that could get us to our destination
#                 if connecting_routes.intersection(destination.route_associations):
#                     possible_stop = self.stops[stop]
#                     #print("\nPossible stop:", possible_stop)

#                     # We need a different one than we already tried in the destination routes
#                     if connecting_routes.difference(destination.route_associations):
#                         routes.append(connecting_routes.difference(destination.route_associations))
#                         routes.append(self.get_routes_for_stops(possible_stop, destination))
                        
#                         break

#             # Since we're starting at the end            
#             routes.insert(0, route)
#         return routes