
from .trace import SignalTrace
from .timestamp import TimeStamp
from . import SignalRecord


def test_find_sample():
    trace = SignalTrace('a')
    print(trace)
    ts = TimeStamp(4)
    nearest = trace.find_nearest_sample(ts)
    assert nearest is None

    sample3 = SignalRecord(TimeStamp(3), 1)
    trace.add(sample3)

    nearest = trace.find_nearest_sample(ts)
    assert nearest is sample3

    sample5 = SignalRecord(TimeStamp(5), 1)
    trace.add(sample5)

    nearest = trace.find_nearest_sample(ts)
    assert nearest is sample3

    sample7 = SignalRecord(TimeStamp(7), 1)
    trace.add(sample7)

    nearest = trace.find_nearest_sample(ts)
    assert nearest is sample3

    sample9 = SignalRecord(TimeStamp(9), 1)
    trace.add(sample9)

    nearest = trace.find_nearest_sample(ts)
    assert nearest is sample3
