import pytest

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
        Stop(id=5, name="E")
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
            Route(name="Green", id=100),
            Route(name="Green B", id=150),
            Route(name="Red", id=200),
            Route(name="Orange", id=300),
            Route(name="Blue", id=400),
        ]

    def get_stops_for_route(self, route_id):
        return STOPS[route_id]

@pytest.fixture
def transit_system_fixture():
    data_provider = TestSystem()
    transit_map = TransitMap(data_provider)
    transit_map.load_stops()

    return transit_map


def test_get_stop_from_string(transit_system_fixture):
    assert transit_system_fixture.get_stop_from_string('C').id == 3


def test_get_route_from_string(transit_system_fixture):
    assert transit_system_fixture.get_route_from_string('Green').id == 100


def test_same_route(transit_system_fixture):
    # Direct Routes
    test_cases = [
        ("A", "B", ["Green"]),
        ("A", "C", ["Green"]),
        ("A", "D", ["Green"]),
        ("A", "E", ["Green"]),
        ("C", "D", ["Green"]),
        ("D", "E", ["Green"]),
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


def test_changeover_routes(transit_system_fixture):
    # Complex Routes
    test_cases = [
        ("A", "G", ["Green", "Red"]),
        ("A", "I", ["Green", "Orange"]),
        ("A", "J", ["Green", "Orange", "Blue"]),
        ("F", "J", ["Red", "Green", "Orange", "Blue"])
    ]

    for test_case in test_cases:
        start, end, expected = test_case

        origin = transit_system_fixture.get_stop_from_string(start)
        destination = transit_system_fixture.get_stop_from_string(end)
        result = transit_system_fixture.get_routes_for_stops(origin, destination)

        assert expected == result
