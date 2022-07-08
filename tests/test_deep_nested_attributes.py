from base import _results


def test_dont_crash_on_deep_nested_attributes():
    code = "a.b.c"
    assert _results(code) == set()
