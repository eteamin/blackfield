from os import path

from blackfield import variables


class Person(object):
    def __init__(self, name, code, image, image_mimetype='png'):
        self.name = name
        self.code = code
        self.image_bytes = image
        self.mimetype = image_mimetype
        self.filename = '%s.%s' % (self.code, self.mimetype)
        self.image_path = path.join(variables.PICTURES, self.filename)
        self._store_image()

    def __repr__(self):
        return '<Person: name=%s, code=%s' % (repr(self.name), repr(self.code))

    def _store_image(self):
        if not path.isfile(self.image_path):
            with open(self.image_path, 'wb') as image:
                image.write(self.image_bytes)
