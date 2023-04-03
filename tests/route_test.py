import pytest
from transit.route import Route
from transit.stop import Stop

@pytest.fixture
def route_fixture() -> Route:
    stop_list = [
        Stop(id=1, name="Foo", route_associations=["Line1"]),
        Stop(id=2, name="Bar", route_associations=["Line1","Line2"]),
        Stop(id=3, name="Baz", route_associations=["Line1"]),
        Stop(id=4, name="Aaaaa", route_associations=["Line1", "Line3"]),
    ]

    r = Route(name="foo", id=1000, stops=stop_list, line_name="testing")    

    return r

def test_has_stop(route_fixture : Route):
    s1 = Stop(id=1, name="Foo", route_associations=["Line1"])
    assert route_fixture.has_stop(s1)

    s2 = Stop(id=4, name="test", route_associations=["Line1"])
    assert route_fixture.has_stop(s2) == False
    

def test_has_stops(route_fixture : Route):
    s1 = Stop(id=1, name="Foo", route_associations=["Line1"])
    s2 = Stop(id=2, name="Bar", route_associations=["Line1","Line2"])
    s3 = Stop(id=3, name="Something", route_associations=["Line1"])

    assert route_fixture.has_stops(s1, s2)
    assert route_fixture.has_stops(s1, s3) == False


def test_get_connecting_stops(route_fixture : Route):
    expected = [
        Stop(id=2, name="Bar", route_associations=["Line1","Line2"]),
        Stop(id=4, name="Aaaaa", route_associations=["Line1", "Line3"])
    ]
    assert route_fixture.get_connecting_stops() == expected


def test_get_connecting_routes(route_fixture : Route):
   assert route_fixture.get_connecting_routes() == ['Line1', 'Line2', 'Line3']
