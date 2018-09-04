import os
import logging
import shutil
import tempfile
import json

from .jsonobj import JsonObj,_JsonObj

logger = logging.getLogger(__name__)


class File(JsonObj):
    def __init__(self, parent, fl, **kwargs):
        kwargs['file'] = fl
        super(File, self).__init__(parent, **kwargs)


def fromLocation(loc):
    loc = os.path.abspath(loc)
    if not isinstance(loc, basestring):
        return
    if not os.path.isdir(loc):
        return
    afile = os.path.join(loc, 'asset.json')
    try:
        return Asset.fromJson(afile)
    except Exception as e:
        logger.exception('%s', e)

class _Asset(_JsonObj):
    def __call__(cls, *args, **kwargs):
        if args and isinstance(args[0], basestring):
            obj = fromLocation(args[0])
            if obj:
                return obj
        return super(_Asset, cls).__call__(*args, **kwargs)


class Asset(JsonObj):
    __metaclass__ = _Asset

    def __init__(self, *args, **kwargs):
        loc = None
        if args:
            if isinstance(args[0], basestring):
                path = os.path.abspath(args[0])
                # if not os.path.isdir(args[0]):
                #     raise TypeError('Cannot find directory {}'.format(args[0]))
                loc = args[0]
        super(Asset, self).__init__(**kwargs)
        self._setLocation(loc)

    def _setLocation(self, loc=None):
        """Initializes the location - do not call from client side.

        :param loc: Path to directory - if None, a temp directory is created.
        :type loc: str | None
        :return: The new location.
        :rtype: str
        """
        if self.parent():
            raise RuntimeError('Cannot set location on descendant')

        if loc is None:
            loc = tempfile.mkdtemp('.asset')
        loc = os.path.abspath(loc)
        self._location = loc
        return self._location

    def location(self):
        return self.root()._location

    def putFile(self, fl, name=None, force=False):
        """Puts file in the asset.

        :param force: If a file w/ the name exists,
        :type force:
        :param fl: Name of file.
        :type fl: str
        :param name: If not None, use this name as the filename.
        :type name: str
        :return: The copied file name.
        :rtype: str
        """
        if not os.path.isfile(fl):
            raise IOError('File {} does not exsit'.format(fl))
        loc = self.initialize()
        lt = set(os.listdir(loc))
        fdir,fname = os.path.split(fl)
        fname = name or fname
        if fname in lt and not force:
            raise ValueError('A file w/ name {} already exists'.format(fname))
        shutil.copy(fl, os.path.join(fdir, fname))


    def initialize(self):
        """If the location of the asset does not exist, create it on disk.

        :return:
        :rtype:
        """
        loc = self.location()
        if not os.path.isdir(loc):
            os.mkdir(loc)
        return loc

    def save(self):
        if not os.path.isdir(self._location):
            os.mkdir(self._location)
        fl = os.path.join(self.location(), 'asset.json')
        self.toJson(fl)
