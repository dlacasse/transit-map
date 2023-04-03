import pytest
from functools import cache

from transit.route import Route
from transit.stop import Stop
from transit.data_providers.base import BaseDataProvider
from transit.system import TransitMap

STOPS = {
    100: [
        Stop(id=1, name="A"),
        Stop(id=2, name="B"),
        Stop(id=3, name="C"),
        Stop(id=4, name="D"),
        Stop(id=5, name="E"),
    ],
    150: [
        Stop(id=11, name="K"),
        Stop(id=2, name="B"),
        Stop(id=3, name="C"),
        Stop(id=4, name="D"),
    ],
    200: [
        Stop(id=6, name="F"),
        Stop(id=3, name="C"),
        Stop(id=7, name="G"),
    ],
    300: [
        Stop(id=8, name="H"),
        Stop(id=4, name="D"),
        Stop(id=9, name="I"),
    ],
    400: [
        Stop(id=9, name="I"),
        Stop(id=10, name="J"),
    ],
}

class TestSystem(BaseDataProvider):
    def get_all_routes(self):
        return [
            Route(name="Green", id=100, line_name="G"),
            Route(name="Green A", id=150, line_name="G"),
            Route(name="Red", id=200, line_name="R"),
            Route(name="Orange", id=300, line_name="O"),
            Route(name="Blue", id=400, line_name="B"),
        ]

    def get_stops_for_route(self, route_id):
        stops = []
        for stop in STOPS[route_id]:
            stops.append(stop)
            
        return stops

@cache
def get_transit_map():
    data_provider = TestSystem()
    transit_map = TransitMap(data_provider)
    transit_map.load_stops()

    return transit_map

@pytest.fixture
def transit_system_fixture():
    return get_transit_map()


def test_get_stop_from_string(transit_system_fixture: TransitMap):
    assert transit_system_fixture.get_stop_from_string('C').id == 3

    with pytest.raises(Exception, match="Unknown Stop!"):
        transit_system_fixture.get_stop_from_string('foo') 


def test_get_route_from_string(transit_system_fixture: TransitMap):
    assert transit_system_fixture.get_route_from_string('Green').id == 100


    with pytest.raises(Exception, match="Unknown Route!"):
        transit_system_fixture.get_route_from_string('bar') 


def test_get_connecting_stops(transit_system_fixture: TransitMap):
   route = transit_system_fixture.get_route_from_string('Green')
   connections = route.get_connecting_stops()

   assert len(connections) == 3
   assert connections[0].name == 'B'
   assert connections[1].name == 'C'
   assert connections[2].name == 'D'


def test_get_routes_with_most_stops(transit_system_fixture: TransitMap):
    assert transit_system_fixture.get_routes_with_most_stops() == [('Green', 5)]


def test_get_routes_with_least_stops(transit_system_fixture: TransitMap):
    assert transit_system_fixture.get_routes_with_least_stops() == [('Blue', 2)]


def test_route_serviced_by_same_line_as_stop(transit_system_fixture: TransitMap):
    route = transit_system_fixture.get_route_from_string('Green')

    stop = transit_system_fixture.get_stop_from_string('B')
    stop2 = transit_system_fixture.get_stop_from_string('C')

    assert transit_system_fixture.route_serviced_by_same_line_as_stop(route, stop)
    assert transit_system_fixture.route_serviced_by_same_line_as_stop(route, stop2) == False


def test_same_route(transit_system_fixture: TransitMap):
    # Direct Routes
    test_cases = [
        ("A", "B", ["Green"]),
        ("A", "C", ["Green"]),
        ("A", "D", ["Green"]),
        ("A", "E", ["Green"]),
        ("C", "D", ["Green"]), 
        ("D", "E", ["Green"]),
        ("K", "B", ["Green A"]),
        ("F", "G", ["Red"]),
        ("H", "D", ["Orange"]),
        ("H", "I", ["Orange"]),
        ("J", "I", ["Blue"]),
        ("I", "J", ["Blue"]),
        ("C", "G", ["Red"])
    ]
    
    for test_case in test_cases:
        start, end, expected = test_case

        origin = transit_system_fixture.get_stop_from_string(start)
        destination = transit_system_fixture.get_stop_from_string(end)
        result = transit_system_fixture.get_routes_for_stops(origin, destination)

        assert expected == result


def test_changeover_routes(transit_system_fixture: TransitMap):
    # Complex Routes (i.e you need to change routes at least once)
    test_cases = [
        ("A", "G", ["Green", "Red"]),
        ("A", "I", ["Green", "Orange"]),
        ("A", "J", ["Green", "Orange", "Blue"]),
        ("F", "J", ["Red", "Green", "Orange", "Blue"]),
        ("E", "K", ["Green", "Green A"]),
    ]

    for test_case in test_cases:
        start, end, expected = test_case

        origin = transit_system_fixture.get_stop_from_string(start)
        destination = transit_system_fixture.get_stop_from_string(end)
        result = transit_system_fixture.get_routes_for_stops(origin, destination)

        assert expected == result
