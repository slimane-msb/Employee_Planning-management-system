import datetime

from src.shift.shift import Shift


def test_shift():
    day = datetime.datetime(2022, 5, 10)
    shift = Shift(day)
    assert shift is not None and shift.date == day


def test_update_length():
    day = datetime.datetime(2022, 5, 10)
    shift = Shift(day)
    shift.add_end("18:30")
    assert shift.length is None
    shift.add_start("18:00")
    assert shift.length == (shift.end_time - shift.start_time)
    shift.add_end("00:30")
    assert shift.length == datetime.timedelta(0, 0, 0, 0, 30, 6)



def test_add_start():
    day = datetime.datetime(2022, 5, 10)
    shift = Shift(day)
    shift.add_start("18:30")
    start_time = datetime.datetime.strptime("18:30:00", "%H:%M:%S")
    assert shift.start_time == start_time


def test_add_end():
    day = datetime.datetime(2022, 5, 10)
    shift = Shift(day)
    shift.add_end("18:30")
    end_time = datetime.datetime.strptime("18:30:00", "%H:%M:%S")
    assert shift.end_time == end_time


def test_add_title():
    day = datetime.datetime(2022, 5, 10)
    shift = Shift(day)
    shift.add_title("cuisine")
    assert shift.title == "cuisine"


def test_shift_str():
    day = datetime.datetime(2022, 5, 10)
    shift = Shift(day)
    shift.add_start("18:30")
    shift.add_end("19:00")
    shift.add_title("cuisine")
    print(str(shift))
    assert True


def test_shift_repr():
    day = datetime.datetime(2022, 5, 10)
    shift = Shift(day)
    shift.add_start("18:30")
    shift.add_end("19:00")
    shift.add_title("cuisine")
    print(repr(shift))
    assert True
