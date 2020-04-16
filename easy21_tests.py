import unittest
from easy21 import *

class Easy21CardTestCase(unittest.TestCase):
    def setUp(self):
        self.card = Card(number=1, color="black")

    def tearDown(self):
        pass
    
    def test_displaying_card(self):
        self.assertEqual(self.card.__str__(), "1 🖤")

    # def test_card_creation_invalid_color(self):
    #     self.assertRaises(AssertionError("Color can only take the values \'red\' or \'black\'"), Card(number=1, color="green"))

    # def test_card_creation_invalid_number(self):
    #     self.assertRaises(AssertionError, Card(number=11, color="black"))

class Easy21DeckTestCase(unittest.TestCase):
    def setUp(self):
       self.deck = Deck()
    
    def test_draw_returns_card(self):
        print(self.deck.draw())
        self.assertTrue(isinstance(self.deck.draw(), Card))

    def test_draw_color_card(self):
        self.assertTrue(self.deck.draw_color_card(color="black").color == "black")


if __name__ == '__main__':
    unittest.main()