from base import lint


def test_multiple_mainloop_calls():
    code = "widget.mainloop();widget.mainloop()"  # Pretty dumb example, but short
    assert lint(code) == {"1:19 TK102 Using multiple `mainloop` calls is totally unnecessary. One call is perfectly enough."}
