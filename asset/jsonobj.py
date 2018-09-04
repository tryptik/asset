import os
import logging
import json
import weakref
import pprint

logger = logging.getLogger(__name__)

class _JsonObj(type):
    _classes = {}

    def __new__(cls, name, bases, dct):
        if name in _JsonObj._classes:
            logger.warn('Redefinition of class %s', name)
        new = super(_JsonObj, cls).__new__(cls, name, bases, dct)
        _JsonObj._classes[name] = new
        return new


class JsonObj(object):
    __metaclass__ = _JsonObj

    def __init__(self, *args, **kwargs):
        self._parent = None
        self._location = None
        self._attrs = {}
        self._children = []
        if args:
            self.setParent(args[0])

        for k, v in kwargs.iteritems():
            self.setAttr(k, v)

    def __str__(self):
        return pprint.pformat(self.toDict())

    def setAttr(self, k, v):
        if v is None:
            self._attrs.pop(k, None)
        else:
            self._attrs[k] = v

    def attr(self, k):
        return self._attrs.get(k)

    def root(self):
        current = self
        parent = current.parent()
        while parent:
            current = parent
            parent = parent.parent()
        return current

    def parent(self):
        return self._parent() if self._parent else None

    def parentIter(self, recursive=False, inclusive=False):
        if inclusive:
            yield self
        parent = self.parent()
        yield parent
        if recursive:
            for pp in parent.parentIter(recursive=True):
                yield pp

    def children(self):
        return list(self._children)

    def childAboutToBeRemoved(self, parent, child):
        pass

    def childAboutToBeAdded(self, parent, child):
        pass

    def beforeReleaseChild(self, child):
        pass

    def beforeAdoptChild(self, child):
        pass

    def setParent(self, other):
        if other:
            if other in self.parentIter(recursive=True, inclusive=True):
                # todo: make hierarchy error
                raise TypeError('Cannot change parent')
            if not isinstance(other, JsonObj):
                raise TypeError('Expected JsonObj, got {}'.format(other.__class__.__name__))
        current = self.parent()
        if current:
            current.beforeReleaseChild(self)
            for p in self.parentIter(recursive=True):
                p.childAboutToBeRemoved(current, self)
            self._parent = None
            current._children = [x for x in current._children if x is not self]

        if other:
            other.beforeAdoptChild(self)
            for p in self.parentIter(recursive=True):
                p.childAboutToBeAdded(other, self)
            self._parent = weakref.ref(other)
            other._children.append(self)

    def row(self):
        parent = self.parent()
        if parent():
            return parent._children.index(self)

    def toDict(self):
        result = {'class': self.__class__.__name__}

        if self._attrs:
            result['attrs'] = dict(self._attrs)
        children = [x.toDict() for x in self.children()]
        if children:
            result['children'] = children
        return result

    def toJson(self, outFile=None, **kwargs):
        data = self.toDict()
        if outFile:
            with open(outFile, 'w') as ot:
                json.dump(data, ot, **kwargs)
        else:
            return json.dumps(data, **kwargs)

    @classmethod
    def fromDict(cls, dct, parent=None):
        clsName = dct['class']
        clsType = _JsonObj._classes.get(clsName, Unknown)

        new = clsType(parent, **dct.get('attrs', {}))
        for ch in dct.get('children', []):
            cls.fromDict(ch, new)
        return new

    @classmethod
    def fromJson(cls, dataOrFile):
        try:
            with open(dataOrFile) as ip:
                data = json.load(ip)
        except:
            data = json.loads(dataOrFile)
        return cls.fromDict(data)

class Unknown(JsonObj):
    def __init__(self, JsonObjPb):
        super(Unknown, self).__init__(JsonObjPb)

    def setParent(self, other):
        raise RuntimeError('Cannot change parent of unknown type')

    def setAttr(self, k, v):
        raise RuntimeError('Cannot setAttr of unknown type')



