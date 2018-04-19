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

    def testProdDB(self):
        conn = sqlite3.connect("ultadata.db")
        cur = conn.cursor()

        sql = 'SELECT DISTINCT Category FROM Products'
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertEqual(len(result_list), 4)

        statement = '''
        SELECT Name, StarRating, Cost, Categories.Category
        FROM Products
        JOIN Categories
        ON Categories.Id = Products.Category
        ORDER BY StarRating
        DESC'''
        categorylist = ["Tool", "Lip", "Eye", "Face"]
        result = cur.execute(statement)
        resultlist = result.fetchall()
        self.assertTrue(resultlist[0][-1] in categorylist) #this tests the joins
        self.assertTrue(float(resultlist[5][1]) <= 5.0)
        self.assertEqual(len(resultlist[0]), 4)
        conn.close()

    def testavbrand(self):
        conn = sqlite3.connect("ultadata.db")
        cur = conn.cursor()

        statement = '''
        SELECT Brand, AVG(StarRating)
        FROM Products
        JOIN Categories
        ON Categories.Id = Products.Category
        WHERE StarRating IS NOT NULL
        GROUP BY Brand
        ORDER BY AVG(StarRating) DESC
        '''
        results = cur.execute(statement)
        result_list = results.fetchall()

        self.assertTrue(len(result_list) < 150)
        self.assertEqual(result_list[0][1], 5.0)

        state = '''SELECT Brand FROM Products GROUP BY Brand'''
        r = cur.execute(state)
        list = r.fetchall()
        self.assertIn(('Revlon',), list)
        self.assertIn(('Maybelline',), list)
        self.assertIn(('ULTA',), list)
        self.assertIn(('BECCA',), list)





unittest.main(verbosity = 2)
