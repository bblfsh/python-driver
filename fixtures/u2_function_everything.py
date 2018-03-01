x = 1
@someann
@someann2(a, b, c)
async def func1(a, b: int, c: int = 3, *d, **e) -> None:
    """
    Docstring
    """
    global x
    x = 2
    y = 1
    l = lambda f, g: f + g

    def func2():
        nonlocal y
        y = 2

    if a:
        yield 1

    return 2, 3, 4
