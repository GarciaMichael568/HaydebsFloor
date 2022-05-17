import unittest
#import haydebsBot
#import haydebsBot
import haydebsBot
#import HaydebsFloor.discordBots.haydebsBot
class TestStringMethods(unittest.TestCase):

    def test_haydeb(self):
        self.assertEqual(haydebsBot.message_to_underscore("!recent lizard rule"), 'lizard_rule')
        
    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

if __name__ == '__main__':
    unittest.main()