from django.test import TestCase


class UnitTesting(TestCase):
	def setUp(self):
		pass

	def test_something(self):
		print('Privet')
		self.assertFalse(False)
		self.assertEqual(1+1, 2)
