

class Person(object):
    def __init__(self, name, code, image):
        self.name = name
        self.code = code
        self.image = image

    def __repr__(self):
        return '<Person: name=%s, person_num=%s' % (repr(self.name), repr(self.code))
