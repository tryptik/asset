import logging
from unittest import TestCase

from google.protobuf import json_format

from asset import AssetPB,Asset

logger = logging.getLogger(__name__)
logging.basicConfig()

class TestAsset(Asset):
    def __init__(self, assetPb=None):
        super(TestAsset, self).__init__(assetPb)


class ProtoTest(TestCase):
    def test_a(self):
        tmp = AssetPB()
        ast = tmp.assets.add()
        tmp.type = 'inkline'
        ast.data['xforms'] = ['a', 'b', 'c']

        ip = tmp.inputs.add()
        ip.name = 'bob_head'
        ip.type = 'joint'

        ip = tmp.inputs.add()
        ip.name = 'bob_neck_a'
        ip.type = 'joint'

        st = json_format.MessageToJson(tmp)
        other = AssetPB()
        json_format.Parse(st, other)

    def test_b(self):
        tast = TestAsset()
        logger.warn('%s', tast)

