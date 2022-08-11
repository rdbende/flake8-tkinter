from base import lint


def test_multiple_mainloop_calls():
    code = "import tkinter;w.mainloop();w.mainloop()"  # Pretty dumb example, but short
    assert lint(code) == {"1:29 TK102 Using multiple mainloop calls is unnecessary. One call is perfectly enough."}
