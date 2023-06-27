wm_attributes_calls = {
    "wm_attributes('-alpha')",
    "attributes('-alpha')",
    "wm_attributes('-alpha', 1)",
    "attributes('-alpha', 1)",
    "wm_attributes('-foo', 1, '-alpha', 1)",
    "attributes('-foo', 1, '-alpha', 1)",
}


def test_wait_visibility_called(lint):
    for attributes in wm_attributes_calls:
        code = f"import tkinter;w.wait_visibility();w.{attributes}"
        assert not lint(code)


def test_wait_visibility_not_called(lint):
    for attributes in wm_attributes_calls:
        code = f"import tkinter;w.{attributes}"
        assert lint(code) == {
            "1:16 TK191 `.wait_visibility()` must be called before setting window transparency on Linux."
        }
