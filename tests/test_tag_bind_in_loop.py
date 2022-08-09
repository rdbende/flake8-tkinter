from base import _results


def test_tag_bind_in_loop_not_storing_tcl_commands():
    code = "for i in range(20):\n  c = widget.tag_bind('<Button-1>', print)"
    assert _results(code) == {"2:7 TK232 Creating tag bindings in a loop can lead to memory leaks. Store the returned command names in a list to clean them up later."}

    code = "while True:\n  c = widget.tag_bind('<Button-1>', print)"
    assert _results(code) == {"2:7 TK232 Creating tag bindings in a loop can lead to memory leaks. Store the returned command names in a list to clean them up later."}

    code = "for i in range(20):\n  widget.tag_bind('<Button-1>', print)\n  [].append()"
    assert _results(code) == {"2:3 TK232 Creating tag bindings in a loop can lead to memory leaks. Store the returned command names in a list to clean them up later."}


def test_tag_bind_in_loop_storing_tcl_commands():
    code = "for i in range(20):\n  c = widget.tag_bind('<Button-1>', print)\n  lista.append(c)"
    assert _results(code) == set()

    code = "while True:\n  c = widget.tag_bind('<Button-1>', print)\n  lista.append(c)"
    assert _results(code) == set()
