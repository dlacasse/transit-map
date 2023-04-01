from transit.system import TransitMap
from transit.data_providers.mbta import MBTADataProvider


if __name__ == "__main__":
    data_provider = MBTADataProvider()
    transit_map = TransitMap(data_provider)
    transit_map.load_stops()

    stop = transit_map.stops['Copley']
    print(transit_map.routes['Green Line B'])       

    origin = transit_map.get_stop_from_string('Copley')
    destination = transit_map.get_stop_from_string('Back Bay')


   