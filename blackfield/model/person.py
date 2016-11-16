

class Person(object):
    def __init__(self, name, code, image):
        self.name = name
        self.code = code
        self.image = image

    def __repr__(self):
        return '<Person: name=%s, code=%s' % (repr(self.name), repr(self.code))
