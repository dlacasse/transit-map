import requests

from transit.data_providers.base import BaseDataProvider
from transit.route import Route
from transit.stop import Stop

class MBTADataProvider(BaseDataProvider):
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