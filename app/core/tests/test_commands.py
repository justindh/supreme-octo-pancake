from unittest.mock import patch
from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import TestCase


class CommandTests(TestCase):
    def test_wait_for_db_ready(self):
        """Test waiting for db when db is available"""
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            # over ride the db get item call to just return true
            gi.return_value = True
            # Call our command
            call_command('wait_for_db')
            # verify we called the getitem exactly one time
            self.assertEqual(gi.call_count, 1)

    # override the wait time to speed up the test
    @patch('time.sleep', return_value=None)
    def test_wait_for_db(self, ts):
        """Test waiting for a db that isnt ready yet but will be"""
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            # return error 5 times and then be true
            gi.side_effect = [OperationalError] * 5 + [True]
            call_command('wait_for_db')
            # verify we called the getitem exactly 6 times
            self.assertEqual(gi.call_count, 6)
