import uuid
import logging
from unittest import TestCase

from google.protobuf import json_format

from asset import AssetPB

logger = logging.getLogger(__name__)
logging.basicConfig()
logger.setLevel(logging.DEBUG)

class ProtoTest(TestCase):
    def test_a(self):
        tmp = AssetPB(id=uuid.uuid4().hex, type='asset')
        ast = tmp.children.add()
        tmp.type = 'inkline'
        ast.data['xforms'] = ['a', 'b', 'c']
        ast.data['test'] = {'this' : 1, 'is' : 3}

        vl = ast.attrs['ints']
        vl = [2,2,2]

        st = json_format.MessageToJson(tmp)
        other = AssetPB()
        json_format.Parse(st, other)

        logger.info('%s', tmp)
