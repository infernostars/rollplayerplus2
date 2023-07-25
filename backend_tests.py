import unittest, time
from backend.utils import (logging, name_generation, text_manipulation)
from backend.classes import repeated_timer
from backend import config


# test with `python3 -m unittest backend_tests.py`


class TestBackend(unittest.TestCase):
    def test_logging(self):
        # This test will pass if 'logging' doesn't raise any Exception.
        try:
            logging.log.debug('Test Debug')
            logging.log.info('Test Info')
            logging.log.warning('Test Warning')
            logging.log.error('Test Error')
        except:
            self.fail("Logging failed")

    def test_name_generation(self):
        names = name_generation.name_generator("greek_city")
        self.assertEqual(len(names), 10, "Name generation failed")

    def test_repeated_timer(self):
        # You might want to adjust the timer interval and assertions
        try:
            timer = repeated_timer.RepeatedTimer(.004, print, "Hello")
            timer.start()
            time.sleep(.01)
            timer.stop()
        except:
            self.fail("Repeated timer failed")

    def test_text_manipulation(self):
        plural = text_manipulation.plural('test', 20)
        self.assertEqual(plural, 'tests', "Text manipulation failed")

    def test_config(self):
        sync_server_option = config.sync_server
        self.assertGreater(int(sync_server_option), 0, "Config value read failed")


if __name__ == '__main__':
    unittest.main()
