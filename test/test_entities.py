from unittest.mock import patch

import services
from entities.pocket import Pocket
from unittest import TestCase

from frames import window_manager

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
