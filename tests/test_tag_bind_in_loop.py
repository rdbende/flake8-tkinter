from base import lint


def test_tag_bind_in_loop_not_storing_tcl_commands():
    code = "import tkinter\nfor i in range(20):\n  c = w.tag_bind('<Button-1>', foo)"
    assert lint(code) == {"3:7 TK232 Creating tag bindings in a loop can lead to memory leaks. Store the returned command names in a list to clean them up later."}

    code = "import tkinter\nwhile True:\n  c = w.tag_bind('<Button-1>', foo)"
    assert lint(code) == {"3:7 TK232 Creating tag bindings in a loop can lead to memory leaks. Store the returned command names in a list to clean them up later."}

    code = "import tkinter\nfor i in range(20):\n  w.tag_bind('<Button-1>', foo)\n  lista.append()"
    assert lint(code) == {"3:3 TK232 Creating tag bindings in a loop can lead to memory leaks. Store the returned command names in a list to clean them up later."}


def test_tag_bind_in_loop_storing_tcl_commands():
    code = "import tkinter\nfor i in range(20):\n  c = w.tag_bind('<Button-1>', foo)\n  lista.append(c)"
    assert lint(code) == set()

    code = "import tkinter\nwhile True:\n  c = w.tag_bind('<Button-1>', foo)\n  lista.append(c)"
    assert lint(code) == set()
