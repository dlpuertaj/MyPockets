import unittest

from entities import pocket
from entities.pocket import Pocket
from unittest import TestCase

class TestEntities(TestCase):

    def setup(self):
        self.pocket = Pocket(1,
                             'Account',
                             10000)

    def test_pocket(self):
        self.assertEqual(self.pocket.get_amount(), 10000)

    if __name__ == "__main__":
        suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestEntities)
        unittest.TextTestRunner().run(suite)