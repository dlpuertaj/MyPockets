from unittest.mock import patch

from entities.pocket import Pocket
from unittest import TestCase


class TestEntities(TestCase):

    def setUp(self):
        with \
                patch('frames.window_manager') as wm\
                :
            self.app = wm.WindowManager()

        self.pocket = Pocket(pocket_id=1,
                             name='Account',
                             amount=10000)

    def test_pocket(self):
        self.assertEqual(self.pocket.get_amount(), 10000)
