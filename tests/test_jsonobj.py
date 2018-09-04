import os
import shutil
import logging
from unittest import TestCase

from google.protobuf import json_format

from asset import JsonObj,Asset

logger = logging.getLogger(__name__)
logging.basicConfig()
logger.setLevel(logging.DEBUG)


class TestAsset(Asset):
    pass

class ProtoTest(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        if hasattr(self, 'tmpDirs'):
            for dr in self.tmpDirs:
                logger.info('  Removing tmp dir: %s', dr)
                shutil.rmtree(dr)

    def test_a(self):
        test = JsonObj(name='test')

        logger.info('%s', test)

    def test_asset(self):
        if 1:
            ast = TestAsset('test.asset')
            loc = ast.location()
            # self.tmpDirs = [loc]
            logger.info('  Created temp dir: %s', loc)
            ast.save()

            self.assertTrue(os.path.isdir(loc))

        if 1:
            ast = Asset('test.asset')
            self.assertTrue(isinstance(ast, TestAsset))