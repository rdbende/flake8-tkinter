def test_use_of_tkinter_dot_message(lint):
    code = "import tkinter;a = tkinter.Message()"
    assert lint(code) == {"1:20 TK251 Using `tkinter.Message` widget. It's redundant since `tkinter.Label` provides the same functionality."}

    code = "import tkinter\nclass Foo(tkinter.Message): ..."
    assert lint(code) == {"2:11 TK251 Using `tkinter.Message` widget. It's redundant since `tkinter.Label` provides the same functionality."}
