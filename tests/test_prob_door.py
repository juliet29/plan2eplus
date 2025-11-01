from datetime import date, time, timedelta, datetime
from replan2eplus.prob_door.interfaces import GeometricDisribution


def test_datetime_addition():
    simple_date = date(2025, 1, 1)
    simple_time = time(1, 0)
    td = 3 * timedelta(minutes=15)
    simple_datetime = datetime.combine(simple_date, simple_time)
    new_datetime = simple_datetime + td
    new_time = new_datetime.time()
    assert new_time == time(1, 45)


def test_sampling_geom_dist():
    X = GeometricDisribution(0.3)
    res = X.sample()
    assert type(res) is int


if __name__ == "__main__":
    test_sampling_geom_dist()
