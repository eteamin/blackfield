from os import path
from shutil import copyfile

from blackfield import variables


class Person(object):
    def __init__(self, name, code, image_bytes=None, image_path=None, image_mimetype='png'):
        if image_bytes:
            assert not image_path
        elif not image_bytes:
            assert image_path
        self.name = name
        self.code = code
        if image_bytes:
            self.image_bytes = image_bytes
            self.mimetype = image_mimetype
            self.filename = '%s.%s' % (self.code, self.mimetype)
            self.store_path = path.join(variables.PICTURES, self.filename)
            self._store_image()
        elif image_path:
            self.image_path = image_path[0]
            self.filename = self.image_path.split('/')[-1].replace(' ', '_')
            self.store_path = path.join(variables.PICTURES, self.filename)
            self._copy_image()

    def __repr__(self):
        return '<Person: name=%s, code=%s' % (repr(self.name), repr(self.code))

    def _store_image(self):
        if not path.isfile(self.store_path):
            with open(self.store_path, 'wb') as image:
                image.write(self.image_bytes)

    def _copy_image(self):
        copyfile(self.image_path, self.store_path)
