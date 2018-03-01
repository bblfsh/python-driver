def func1():
    def func2(): pass
    func2()

def func3():
    def func4(): pass
    func4()

def func5():
    def func6():
        def func7(): pass
        func7()
    func6()

def func8():
    a = 1
    def func9():
        nonlocal a
        a = 2
    func9()
