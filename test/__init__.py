import unittest

from entities.pocket import Pocket
from test.test_entities import TestEntities

if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestEntities)
    unittest.TextTestRunner().run(suite)