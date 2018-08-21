import os
import logging
from google.protobuf import json_format
from .asset_pb2 import AssetPB


logger = logging.getLogger(__name__)

class _Asset(type):
    _classes = {}

    def __new__(cls, name, bases, dct):
        if name in _Asset._classes:
            logger.warn('Redefinition of class %s', name)
        new = super(_Asset, cls).__new__(cls, name, bases, dct)
        _Asset._classes[name] = new
        return new


class Asset(object):
    __metaclass__ = _Asset
    def __init__(self, assetPb=None):
        self.__asset = assetPb
        if not self.__asset:
            self.__asset = AssetPB()
            self.__asset.type = self.__class__.__name__

    def __str__(self):
        return self.__asset.__str__()

    def toJson(self, outFile=None):
        if outFile:
            with open(outFile, 'w') as ot:
                ot.write(json_format.MessageToJson(self.__asset))
        else:
            return json_format.MessageToJson(self.__asset)

    @classmethod
    def fromJson(cls, dataOrFile):
        tmp = AssetPB()
        if os.path.isfile(dataOrFile):
            with open(dataOrFile) as ip:
                json_format.Parse(ip.read(), tmp)
        else:
            json_format.Parse(dataOrFile, tmp)
        clsType = _Asset._classes.get(tmp.type, Unknown)
        return clsType(tmp)

class Unknown(Asset):
    def __init__(self, assetPb):
        super(Unknown, self).__init__(assetPb)

