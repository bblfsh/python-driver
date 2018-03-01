@somedecorator
def func1(): pass

@somedecorator(1, 2, 3)
def func2(): pass

@somedecorator
@somedecorator(4, 5, 6)
def func3(): pass
