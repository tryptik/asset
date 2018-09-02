import re,StringIO,logging,weakref
from contextlib import contextmanager

logger = logging.getLogger(__name__)

from .edgeset import EdgeSet
from .item import Item

@contextmanager
def setLayer(definition, layerName):
    index = definition._currentLayer
    definition.setCurrentLayer(layerName)
    try:
        yield definition
    finally:
        definition._currentLayer = index

class Visitor(object):
    def visit(self, item):
        if self.start(item):
            for ch in item.childIter():
                self.visit(ch)
        self.end(item)

    def start(self, item):
        return True

    def end(self, item):
        pass


class PFormat(Visitor):
    def __init__(self):
        self.buf = StringIO.StringIO()

    def start(self, item):
        self.buf.write(item.path())
        self.buf.write('\n')
        return True


class Base(Item):
    def name(self):
        return self.data('name', '')

    def path(self):
        return '/'.join(reversed([x.name() for x in self.parentIter(recursive=True, inclusive=True)]))

    def pformat(self):
        vis = PFormat()
        vis.visit(self)
        return vis.buf.getvalue()

    # def childIter(self, recursive=False, inclusive=False):
    #     root = self.root()
    #     cl = root.currentLayer()
    #     for ch in super(Base, self).childIter(recursive, inclusive):
    #         if ch in cl:
    #             yield ch

    def childByName(self, name):
        for ch in self.childIter():
            if ch.name() == name:
                return ch

class Layer(object):
    def __init__(self, definition):
        self._definiton = weakref.ref(definition)

    def name(self):
        return 'Default'

    def __contains__(self, item):
        return True

    def add(self, node):
        pass

    def  definition(self):
        return self._definiton()

class NodeLayer(Layer):
    def __init__(self, definition, name):
        super(NodeLayer, self).__init__(definition)
        assert(name != 'Default')
        self._name = name
        self._nodes = set()

    def name(self):
        return self._name

    def add(self, *nodes):
        definition = self.definition()
        for node in nodes:
            assert(node.root() is definition)
            for p in node.parentIter(recursive=True, inclusive=True):
                self._nodes.add(node)

    def __contains__(self, item):
        return item in self._nodes

class Variation(Base):
    pass

class ComponentVariation(Variation):
    pass

class GeometryVariation(Variation):
    pass

class LookDevVariation(Variation):
    pass

class TextureVariation(Variation):
    pass


class VariationGroup(Base):
    def acceptsChild(self, other):
        return isinstance(other, Variation)

    def getVariation(self, name):
        for k in self.childIter():
            if k.data('name') == name:
                return k

    def _addVariation(self, cls, name, **data):
        if self.getVariation(name):
            raise ValueError('A variation with name "{}" already exists'.format(name))
        nl = cls(self, name=name, **data)
        assert(nl.parent() is self)
        return nl

class ComponentVariationGroup(VariationGroup):
    def acceptsChild(self, other):
        return isinstance(other, ComponentVariation)

    def addVariation(self, name, spref, **data):
        data['spref'] = spref
        nl = self._addVariation(ComponentVariation, name, **data)
        return nl

class GeometryVariationGroup(VariationGroup):
    def acceptsChild(self, other):
        return isinstance(other, GeometryVariation)

    def addVariation(self, name, **data):
        nl = self._addVariation(GeometryVariation, name, **data)
        return nl

    def collectShapes(self):
        result = []
        for x in self.childIter():
            shapes = x.data('shapes', [])
            result.extend(x.data('shapes', []))
        return list(set(result))

class TextureVariationGroup(VariationGroup):
    def acceptsChild(self, other):
        return isinstance(other, TextureVariation)

    def addVariation(self, name, **data):
        nl = self._addVariation(TextureVariation, name, **data)
        return nl

class LookDevVariationGroup(VariationGroup):
    def acceptsChild(self, other):
        return isinstance(other, LookDevVariation)

    def addVariation(self, name, **data):
        nl = self._addVariation(LookDevVariation, name, **data)
        return nl


class Definition(Base):
    def __init__(self):
        super(Definition, self).__init__()
        self._layers = [Layer(self)]
        self._currentLayer = 0

    def acceptsChild(self, other):
        return isinstance(other, (VariationGroup, Layer,))

    def addLayer(self, name):
        assert not re.search('[^a-zA-Z0-9_]', name)
        assert name not in self._layers
        nl = NodeLayer(self, name)
        self._currentLayer = len(self._layers)
        self._layers.append(nl)
        return nl

    def layer(self, name):
        for i,x in enumerate(self._layers):
            if x.name() == name:
                return x

    def layerIndex(self, name):
        for i,x in enumerate(self._layers):
            if x.name() == name:
                return i
        return -1

    def setCurrentLayer(self, name):
        if name is None:
            self._currentLayer = 0
        else:
            lindex = self.layerIndex(name)
            if lindex < 0:
                raise ValueError('Could not locate layer "{}"'.format(name))
            self._currentLayer = lindex

    def currentLayer(self):
        return self._layers[self._currentLayer]

    def addGroup(self, type, name):
        if self.childByName(name):
            raise ValueError('A group with name "{}" already exists'.format(name))
        if type == 'Component':
            grp = ComponentVariationGroup(self, name=name)
        elif type == 'Geometry':
            grp = GeometryVariationGroup(self, name=name)
        elif type == 'Texture':
            grp = TextureVariationGroup(self, name=name)
        elif type == 'LookDev':
            grp = LookDevVariationGroup(self, name=name)
        else:
            raise ValueError('Invalid group type "{}"'.format(type))

        return grp

    def getAllVariations(self):
        result = []
        for it in self.childIter(recursive=True):
            if not it.numChildren():
                result.append(it)
        return result

    def findVariation(self, path):
        toks = [x for x in path.split('/') if x]
        current = self
        for tok in toks:
            current = current.childByName(tok)
            if not current:
                return
        return current

    def filterVariations(self, *values, **kwargs):
        """Returns any variation paths that are not valid for the supplied layer.

        :param values: Variation paths to validate.
        :type values: str
        :keyword layerName: The name of the layer to use or None
        :type kwargs: str | None
        :return: A list of the paths that are not valid or settable.
        :rtype: list
        """
        result = []
        with setLayer(self, kwargs.get('layerName')):
            for value in values:
                var = self.findVariation(value)
                if not var:
                    result.append(value)
        return result

