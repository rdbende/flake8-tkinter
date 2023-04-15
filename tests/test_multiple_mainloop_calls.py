from base import lint


def test_multiple_mainloop_calls():
    code = "import tkinter\ndef foo():\n\ttop.mainloop()\nroot.mainloop()"
    assert lint(code) == {"4:1 TK102 Using multiple mainloop calls is unnecessary. One call is perfectly enough."}

def test_second_mainloop_call_inside_if_name_equals_main():
    code = "import tkinter;w.mainloop()\nif __name == '__main__':w.mainloop()"
    assert not lint(code)
