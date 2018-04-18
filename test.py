from ulta import *
import unittest
from random import randint

class TestData(unittest.TestCase):

    def testeyeListLen(self):
        eyelist = getAllProdType("eyes", "48")
        firstobj = eyelist[0]
        categorylist = ["1", "2", "3", "4"]

        self.assertEqual(len(eyelist), 48)
        self.assertEqual(len(firstobj), 11)
        self.assertEqual(len(eyelist[randint(0, 47)]), 11)
        self.assertTrue("https://www.ulta.com/" in eyelist[0][-1])
        self.assertTrue(eyelist[2][2] in categorylist)
        self.assertTrue(float(eyelist[-1][8]) <= 5.0)

    def testTool(self):
        toollist = getAllProdType("tools", "48")
        categorylist = ["1", "2", "3", "4"]

        self.assertEqual(len(toollist), 48)
        self.assertEqual(len(toollist[0]), 11)
        self.assertEqual(len(toollist[randint(0, 47)]), 11)
        self.assertTrue("https://www.ulta.com/" in toollist[0][-1])
        self.assertTrue(toollist[2][2] in categorylist)
        self.assertTrue(float(toollist[-1][8]) <= 5.0)

    def testFace(self):
        facelist = getAllProdType("face", "48")
        categorylist = ["1", "2", "3", "4"]

        self.assertEqual(len(facelist), 48)
        self.assertEqual(len(facelist[0]), 11)
        self.assertEqual(len(facelist[randint(0, 47)]), 11)
        self.assertTrue("https://www.ulta.com/" in facelist[0][-1])
        self.assertTrue(facelist[2][2] in categorylist)
        self.assertTrue(float(facelist[-1][8]) <= 5.0)

    def testLip(self):
        liplist = getAllProdType("lips", "48")
        categorylist = ["1", "2", "3", "4"]

        self.assertEqual(len(liplist), 48)
        self.assertEqual(len(liplist[0]), 11)
        self.assertEqual(len(liplist[randint(0, 47)]), 11)
        self.assertTrue("https://www.ulta.com/" in liplist[0][-1])
        self.assertTrue(liplist[2][2] in categorylist)
        self.assertTrue(float(liplist[-1][8]) <= 5.0)

class TestSQL(unittest.TestCase):
    


unittest.main(verbosity = 2)
