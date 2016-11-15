

class Person(object):
    def __init__(self, name, person_num, image):
        self.name = name
        self.person_num = person_num
        self.image = image

    def __repr__(self):
        return '<Person: name=%s, person_num=%s' % (repr(self.name), repr(self.person_num))
