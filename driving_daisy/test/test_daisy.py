from unittest import TestCase

from driving_daisy.driver import get_command

class RETests(TestCase):

    def test_tweet_full(self):
        self.assertEquals(
            get_command(r"#daisy forward"), "f")

    def test_tweet_full_spacing(self):
        self.assertEquals(
            get_command(r"#daisy  back"), "b")

    def test_tweet_full_extra_junk(self):
        self.assertEquals(
            get_command(r" junk   #daisy left"), "l")

    def test_tweet_short(self):
        self.assertEquals(
            get_command(r"#daisy r"), "r")
