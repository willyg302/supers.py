import unittest

from supers import *


class TestWatch(unittest.TestCase):

	def setUp(self):
		self.d = {'a': 1, 'b': 2, 'd': {'e': 5, 'f': 6}}
		self.l = [1, 'b', {'a': 'a', 'b': ['c', 'd', 'e']}, 2009]
		self.callbacks = 0

	def callback(self, record):
		self.callbacks += 1
		# print '{} {} --> {} on path {}'.format(record['type'], record['oldvalue'], record['value'], record['path'])

	def test_dict(self):
		n = watch(self.d, self.callback)
		n['c'] = 3
		del n['d']['e']
		self.assertEqual(self.callbacks, 2)

	def test_from_dict(self):
		n = NotifyDict.from_dict(self.d).on('change', self.callback)
		n['x'] = {'y': 8, 'z': 9}
		n['x']['z'] = 10
		del n['x']
		self.assertEqual(self.callbacks, 3)

	def test_list(self):
		n = watch(self.l, self.callback).on('delete', self.callback).on('change [1].b', self.callback)
		del n[1]
		n[1]['c'] = 'Hello!'
		n[2] -= 1
		n[1]['b'][2] += 'lephant'
		del n[1]
		n.insert(0, 'puppies')
		self.assertEqual(self.callbacks, 9)


if __name__ == '__main__':
	unittest.main()