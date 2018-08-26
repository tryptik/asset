import uuid
import os
import json
import weakref
import logging

from .edgeset import EdgeSet

logger = logging.getLogger(__name__)

ALLOW_CLASS_REDEFINITION = True

class _Item(type):
    _classes = {}
    def __new__(cls, name, bases, dct):
        if name in _Item._classes:
            if not ALLOW_CLASS_REDEFINITION:
                raise ValueError('Class {0} already defined'.format(name))
            logger.warn('Redefinition of class %s', name)
        new = type.__new__(cls, name, bases, dct)
        _Item._classes[name] = new
        return new

class ItemBase(object):
    __metaclass__ = _Item

    edges = EdgeSet()

    _context = None

    def __init__(self):
        self._parent = None
        self._children = []
        self._data = {}
        self._id = uuid.uuid4().hex

    @staticmethod
    def context():
        return ItemBase._context

    @staticmethod
    def setContext(ctx):
        old = ItemBase._context
        ItemBase._context = ctx
        return old

    def id(self):
        return self._id

    def parent(self):
        return self._parent() if self._parent else None

    def row(self):
        parent = self.parent()
        if parent:
            return parent._children.index(self)
        return -1

    def parentIter(self, recursive=False, inclusive=False):
        if inclusive:
            yield self
        parent = self.parent()
        if parent:
            yield parent

            if recursive:
                for par in parent.parentIter(recursive=True):
                    yield par

    def childIter(self, recursive=False, inclusive=False):
        if inclusive:
            yield self
        for ch in self._children:
            yield ch
            if recursive:
                for chi in ch.childIter(recursive=True):
                    yield chi

    def numChildren(self):
        return len(self._children)

    def root(self):
        last = self
        for p in self.parentIter(recursive=True):
            last = p
        return last

    def acceptsChild(self, other):
        return False

    def acceptsParent(self, other):
        return True

    def row(self):
        par = self.parent()
        if par:
            return par._children.index(self)
        return -1

    def listData(self):
        return self._data.keys()

    def data(self, key, default=None):
        return self._data.get(key, default)

    def findData(self, key, default=None):
        for p in self.parentIter(True, True):
            if p.hasData(key):
                return p.data(key)
        return default

    def hasData(self, key):
        return key in self._data

    def inputIter(self, recursive=False, inclusive=False):
        for ip in ItemBase.edges.inputIter(self, recursive, inclusive):
            yield ip

    def outputIter(self, recursive=False, inclusive=False):
        for op in ItemBase.edges.outputIter(self, recursive, inclusive):
            yield op

    def hasInput(self):
        for r in self.inputIter():
            return True
        return False

    def hasOutput(self):
        for r in self.outputIter():
            return True
        return False

    def toDict(self, conns=None):
        result = {'__id__' : self.id(), '__class__' : self.__class__.__name__}
        if self._data:
            result['__data__'] = dict(self._data)
        dcons = conns is None

        if dcons:
            conns = conns or []
        ch = self._childItemsForExport(conns)

        if ch:
            result['__children__'] = ch

        for ip in self.inputIter():
            conns.append([ip.id(), self.id()])
        for op in self.outputIter():
            conns.append([self.id(), op.id()])
        if dcons and conns:
            result['__conns__'] = conns
        return result

    def toJson(self, outFile=None, **kwargs):
        if outFile:
            with open(outFile, 'w') as op:
                json.dump(self.toDict(), op, **kwargs)
        else:
            return json.dumps(self.toDict(), **kwargs)

    def _childItemsForExport(self, conns):
        return [x.toDict(conns) for x in self.childIter()]

    @staticmethod
    def findClass(name):
        return _Item._classes.get(name, _Item._classes['Unknown'])

    @classmethod
    def fromJson(cls, arg):
        if os.path.isfile(arg):
            with open(arg) as ip:
                data = json.load(ip)
        else:
            data = json.loads(arg)
        return cls.fromDict(data)

    @classmethod
    def fromDict(cls, data, parent=None):
        ctx = cls.setContext('fromDict')
        try:
            return cls._fromDict(data, parent)
        finally:
            if not ctx:
                cls.setContext(ctx)

    @classmethod
    def _fromDict(cls, data, parent=None, bldData=None, conns=None):
        bldData = bldData or {}
        conns = conns or []
        clsName = data.get('__class__', 'Unknown')
        clsType = _Item._classes.get(clsName, _Item._classes['Unknown'])
        nid = data['__id__']
        new = clsType()
        bldData[nid] = new
        new._data = data.get('__data__', {})

        if parent:
            if 'name' in new._data:
                new._data['name'] = clsType._getNewName(new._data['name'], parent)
            new._parent = weakref.ref(parent)
            parent._appendChild(new)

        refData = data.get('__ref__')
        if refData:
            cls._refFromDict(refData)

        conns = data.get('__conns__', [])

        for ch in data.get('__children__', []):
            cls._fromDict(ch, new, bldData, conns)

        for src,dest in conns:
            osrc = bldData.get(src)
            odest = bldData.get(dest)
            if osrc and odest:
                if not osrc.isConnectedTo(odest):
                    osrc.connectTo(odest)
        return new

    @classmethod
    def refFromDict(cls, data):
        pass

    def childAdded(self, parent, child):
        pass

    def childRemoved(self, parent, child):
        pass

    def dataChanged(self, item, key, old, new):
        pass

    def connectionMade(self, src, dest):
        pass

    def connectionBroken(self, src, dest):
        pass


class Unknown(ItemBase):
    pass


class Item(ItemBase):
    def __init__(self, *args, **kwargs):
        ItemBase.__init__(self)

        for k,v in kwargs.iteritems():
            self.setData(k, v)

        if args:
            if len(args) > 1:
                raise ValueError('Expected 0 or 1 arg, got {0}'.format(len(args)))
            self.setParent(args[0])

    @staticmethod
    def coreType():
        return 'Item'

    def isConnectedTo(self, dest):
        return dest in self.outputIter()

    def connectTo(self, dest):
        Item.edges.addEdge(self, dest)
        for p in self.parentIter(recursive=True, inclusive=True):
            p.connectionMade(self, dest)
        return self

    def disconnect(self, dest):
        Item.edges.rmEdge(self, dest)
        for p in self.parentIter(recursive=True, inclusive=True):
            p.connectionBroken(self, dest)
        return self

    def __rshift__(self, dest):
        return self.connectTo(dest)

    def __ior__(self, dest):
        return self.disconnect(dest)

    def _appendChild(self, child):
        child._parent = weakref.ref(self)
        self._children.append(child)
        # todo: turn this back on
        # for p in self.parentIter(recursive=True, inclusive=True):
        #     p.childAdded(self, child)

    def _releaseChild(self, child):
        child._parent = None
        self._children = [x for x in self._children if x is not child]
        for p in self.parentIter(recursive=True, inclusive=True):
            p.childRemoved(self, child)

    def setParent(self, other=None):
        if other is self.parent():
            return
        if other:
            if not other.acceptsChild(self):
                raise ValueError('{0} does not accept {1}'.format(other.__class__, self.__class__))
            if not self.acceptsParent(other):
                raise ValueError
            if other in self.parentIter(recursive=True):
                raise ValueError
        current = self.parent()
        if current:
            current._releaseChild(self)
        if other:
            other._appendChild(self)
            assert(self in other._children)

    def setData(self, key, value):
        """Set a piece of data.

        :param key: The name of the datum to set.
        :type key: str
        :param value: The value of the datum. If None, data is cleared from the internal store.
        :type value: object
        :param mute: If True, do not send dataChanged notification.
        :type mute: bool
        :return: The original value of the data.
        :rtype: object
        """
        cr = self._data.get(key)
        if cr is None and value is None:
            return
        if value == cr:
            return
        if value is None:
            self._data.pop(key)
        else:
            self._data[key] = value

        for p in self.parentIter(recursive=True):
            p.dataChanged(self, key, cr, value)

        return cr
