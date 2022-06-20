from base import _results


def test_time_sleep():
    code = "import time\ntime.sleep()"
    assert _results(code) == {"2:1 TK030 time.sleep used; use tkinter.widget.after instead"}


def test_from_time_sleep():
    code = "from time import sleep\nsleep()"
    assert _results(code) == {"2:1 TK030 time.sleep used; use tkinter.widget.after instead"}


def test_from_relative_time_sleep():
    code = "from .time import sleep\nsleep()"
    assert _results(code) == set()


def test_relative_time_sleep_after_real_time_sleep():
    code = "from time import sleep\nfrom .time import sleep\nsleep()"
    assert _results(code) == set()


def test_redefinition_of_time_sleep():
    code = "import tkinter\nfrom time import sleep\nsleep()\ndef sleep(): pass\nsleep()"
    assert _results(code) == {"3:1 TK030 time.sleep used; use tkinter.widget.after instead"}
