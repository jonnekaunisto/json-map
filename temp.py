class BaseClass(object):
    def __new__(cls, initval=None, name='var'):
        print(cls)
        print("here")
        obj = super(BaseClass, cls).__new__(cls)
        obj.hurrdurr = "set"
        return obj

    def __init__(self):
        print("in init")


class RevealAccess(BaseClass):
    """A data descriptor that sets and returns values
       normally and prints a message logging their access.
    """

    def __init__(self, initval=None, name='var'):
        print('hi')
        self.val = initval
        self.name = name

    def __setattr__(self, name, value):
        print(name)
        print(value)
        object.__setattr__(self, name, value)


m = RevealAccess(initval=1)
print(m.__dict__)
print(m.val)
m.val = 20
print(m.hurrdurr)
