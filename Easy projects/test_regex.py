import unittest
from regex import search


class MyTestCase(unittest.TestCase):

	def test_search(self):
		self.assertTrue(search('colou?r', 'color'))
		self.assertTrue(search('colou?r', 'colour'))
		self.assertFalse(search('colou?r', 'colouur'))
		self.assertTrue(search('colou*r', 'color'))
		self.assertTrue(search('col.*r', 'color'))
		self.assertTrue(search('col.*r', 'colour'))
		self.assertTrue(search('col.*r', 'colr'))
		self.assertTrue(search('col.*r', 'collar'))
		self.assertFalse(search('col.*r$', 'colors'))  #
		self.assertFalse(search('^apple$', 'apple pie'))
		self.assertTrue(search('^ apple$', ' apple'))  #
		self.assertTrue(search('^ apple$', ' apple'))
		self.assertTrue(search('^apple$', 'apple'))
		self.assertFalse(search('^apple$', 'apple pie'))
		self.assertTrue(search('.$', ' apple'))


if __name__ == '__main__':
	unittest.main()
