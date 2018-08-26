import logging
from unittest import TestCase

from google.protobuf import json_format

from variations import *

logger = logging.getLogger(__name__)
logging.basicConfig()
logger.setLevel(logging.DEBUG)

class VarTest(TestCase):
    def test_aa(self):

        df = Definition()

        grp = df.addGroup('Component', 'hat')
        self.assertRaises(Exception, df.addGroup, 'Component', 'hat')

        cowboyHat = grp.addVariation('cowboy', '{spref:show/shot/hat_cowboy.cmpt')

        self.assertTrue(cowboyHat in grp.childIter())

        fedoraHat = grp.addVariation('fedora', '{spref:show/shot/hat_fedora.cmpt')

        grp = df.addGroup('Component', 'pants')
        cowboyJeans = grp.addVariation('cowboy', '{spref:show/shot/pants_cowboy.cmpt')
        suitPants = grp.addVariation('suit', '{spref:show/shot/pants_suit.cmpt')
        shortPants = grp.addVariation('short', '{spref:show/shot/shorts_suit.cmpt')


        logger.info(df.pformat())

        self.assertTrue(list(df.childIter()))

        tmp = df.getAllVariations()
        self.assertEqual(len(tmp), 5)

        ly = df.addLayer('city')
        dt = df.pformat()
        logger.info(df.pformat())

        self.assertTrue(ly is df.currentLayer())
        self.assertEqual('city', df.currentLayer().name())

        tmp = df.getAllVariations()
        self.assertEqual(len(tmp), 0)

        ly.add(fedoraHat)
        ly.add(suitPants, shortPants)

        ch = list(df.childIter())
        tmp = df.getAllVariations()
        self.assertEqual(len(tmp), 3)

        logger.info('-' * 40)
        for k in df.getAllVariations():
            logger.info('  -  %s', k.path())

        badVars = df.filterVariations('/hat/fedora', '/pants/suit', '/bad/path')
        self.assertEqual(['/bad/path'], badVars)

        sword = df.addGroup('Geometry', 'misc')
        longSV = sword.addVariation('longSword', shapes=['ac_cn_hi_longSwordShape'])
        shortSV = sword.addVariation('shortSword', shapes=['ac_cn_hi_shortSwordShape'])

        self.assertTrue(longSV.parent() is sword)
        self.assertTrue(shortSV.parent() is sword)

        self.assertTrue(shortSV in sword.childIter())
        self.assertTrue(longSV in sword.childIter())

        self.assertEqual(['ac_cn_hi_shortSwordShape'], shortSV.data('shapes'))

        self.assertTrue(sword.collectShapes())



