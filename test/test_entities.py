import unittest

from entities import pocket
from entities.pocket import Pocket
from unittest import TestCase

class TestEntities(TestCase):

    def setUp(self):
        self.pocket = Pocket(pocket_id=1,
                             name='Account',
                             amount=10000)

    def test_pocket(self):
        self.assertEqual(self.pocket.get_amount(), 10000)
