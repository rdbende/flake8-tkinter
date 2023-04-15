from base import lint


def test_multiple_mainloop_calls():
    code = "import tkinter\nw.mainloop()\nw.mainloop()"
    # One would probably call the second mainloop inside the first mainloop, but this test works just as well
    assert lint(code) == {"3:1 TK102 Using multiple mainloop calls is unnecessary. One call is perfectly enough."}

def test_second_mainloop_call_inside_if_name_equals_main():
    code = "import tkinter;w.mainloop()\nif __name == '__main__':w.mainloop()"
    # One would probably call the second mainloop inside the first mainloop, but this test works just as well
    assert not lint(code)
