import weakref

class CycleError(Exception):
    pass

class ConnectionExistsError(Exception):
    pass

class DoubleConnectionError(Exception):
    pass

class ConnectionDoesNotExistError(Exception):
    pass

class DAGEdgeSet(object):
    def __init__(self):
        # parent
        self._inputs = {}
        self._outputs = {}

    def addEdge(self, source, dest):
        self._inputs[dest] = source
        self._outputs.setdefault(source, []).append(dest)

    def rmEdge(self, source, dest):
        self._inputs.pop(dest, None)
        tmp = [x for x in self._outputs.get(source, []) if x is not source]
        self._outputs[source] = tmp


class EdgeSet(object):
    def __init__(self):
        self._inputs = {}
        self._outputs = {}

    def pop(self, item):
        result = set()
        for k in self._inputs.pop(item, []):
            result.add((k, item,))
        for k in self._outputs.pop(item, []):
            result.add((item, k,))
        return result

    def edgeIter(self):
        for k, v in self._inputs.items():
            for i in v:
                yield (i, k)

    def __iter__(self):
        return self.edgeIter()

    def addEdge(self, source, dest, errIfExists=True):
        if self.hasEdge(dest, source):
            raise DoubleConnectionError
        if dest in self.inputIter(source):
            raise CycleError

        if self.hasEdge(source, dest):
            if errIfExists:
                raise ConnectionExistsError('%s is already connected to %s' % (source, dest))
            return

        self._inputs.setdefault(dest, []).append(source)
        self._outputs.setdefault(source, []).append(dest)

    def rmEdge(self, source, dest):
        if not self.hasEdge(source, dest):
            raise ConnectionDoesNotExistError('%s and %s are not connected' % (source, dest))

        self._inputs[dest].remove(source)
        self._outputs[source].remove(dest)

    def hasEdge(self, source, dest):
        return source in self._inputs.get(dest, [])

    def hasInput(self, dest):
        for ip in self.inputIter(dest):
            return True
        return False

    def hasOutput(self, source):
        for op in self.outputIter(source):
            return True
        return False

    def getInputs(self, node, typ=None):
        if typ:
            return [x for x in self._inputs.get(node, []) if isinstance(x, typ)]
        return self._inputs.get(node, [])

    def getOutputs(self, node, typ=None):
        if typ:
            return [x for x in self._outputs.get(node, []) if isinstance(x, typ)]
        return self._outputs.get(node, [])

    def inputIter(self, node, recursive=False, inclusive=False):
        if inclusive:
            yield node
        for e in self.getInputs(node):
            yield e
            if recursive:
                for oe in self.inputIter(e, recursive=True):
                    yield oe

    def outputIter(self, node, recursive=False, inclusive=False):
        if inclusive:
            yield node
        for e in self.getOutputs(node):
            yield e
            if recursive:
                for oe in self.outputIter(e, recursive=True):
                    yield oe

    def sortOutputs(self, node, cmpfunc):
        self._outputs.get(node, []).sort(cmpfunc)

    def getConnections(self, item):
        """Return all edges that contain item as source or dest
        """
        result = set()
        for ip in self._inputs.get(item, []):
            result.add((ip, item,))
        for op in self._outputs.get(item, []):
            result.add((item, op,))
        return result

    def rmInputs(self, node):
        for ip in self.getInputs(node):
            self.rmEdge(ip, node)

    def rmOutputs(self, node):
        for ip in self.getOutputs(node):
            self.rmEdge(node, ip)

