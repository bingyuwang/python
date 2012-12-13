class bird():
    feather = True

class flybird(bird):
    fly = False
    def __init__(self, age):
        self.age = age
    def __getattr__(self, name):
        if name == 'adult':
            if self.age > 1:
                return True
            else:
                return False
        else:
            raise AttributeError(name)

i = flybird(2)

print bird.__dict__
print flybird.__dict__
print i.adult
i.age = 0
print i.adult
