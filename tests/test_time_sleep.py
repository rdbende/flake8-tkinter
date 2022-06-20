from base import _results


def test_time_sleep():
    code = "import time\ntime.sleep(10)"
    assert _results(code) == {
        "2:1 TK030 'time.sleep(10)' used, since it blocks the thread and the GUI will freeze. Use the '.after(milliseconds)' method instead, which isavailable on every Tkinter widget"
    }


def test_from_time_sleep():
    code = "from time import sleep\nsleep(10)"
    assert _results(code) == {
        "2:1 TK030 'time.sleep(10)' used, since it blocks the thread and the GUI will freeze. Use the '.after(milliseconds)' method instead, which isavailable on every Tkinter widget"
    }


def test_from_relative_time_sleep():
    code = "from .time import sleep\nsleep()"
    assert _results(code) == set()


def test_relative_time_sleep_after_real_time_sleep():
    code = "from time import sleep\nfrom .time import sleep\nsleep()"
    assert _results(code) == set()


def test_redefinition_of_time_sleep():
    code = "import tkinter\nfrom time import sleep\nsleep(10)\ndef sleep(): pass\nsleep(10)"
    assert _results(code) == {
        "3:1 TK030 'time.sleep(10)' used, since it blocks the thread and the GUI will freeze. Use the '.after(milliseconds)' method instead, which isavailable on every Tkinter widget"
    }
