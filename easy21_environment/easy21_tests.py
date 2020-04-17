import unittest
from easy21 import *

class Easy21CardTestCase(unittest.TestCase):
    def setUp(self):
        self.card = Card(number=1, color="black")
    
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
        self.assertTrue(isinstance(self.deck.draw(), Card))

    def test_draw_color_card(self):
        self.assertTrue(self.deck.draw_color_card(color="black").color == "black")

class Easy21GameEnvironmentTestCase(unittest.TestCase):
    def setUp(self):
        self.env = Easy21GameEnvironment()
        self.env.current_state = (10, 1)

    def test_reward_player_busts(self):
        self.env.current_state = (10, 22)
        reward = self.env.reward(self.env.current_state)
        self.assertTrue(self.env.done) # game ends
        self.assertTrue(reward == -1)

    def test_reward_draw(self):
        self.env.current_state = (9, 17)
        self.env.done = True
        self.env.dealers_sum = 17
        self.assertTrue(self.env.reward(self.env.current_state) == 0)
    
    def test_reward_win(self):
        self.env.current_state = (10, 21)
        self.env.done = True
        self.env.dealers_sum = 14
        self.assertTrue(self.env.reward(self.env.current_state) == 1)
    
    def test_dealer_acts_less_than_17(self):
        self.env.dealers_sum = 16
        self.env.dealer_acts()
        self.assertTrue(self.env.dealers_sum != 16)
    
    def test_dealer_acts_greater_than_17(self):
        self.env.dealers_sum = 18
        self.env.dealer_acts()
        self.assertTrue(self.env.dealers_sum == 18)

    def test_evaluate_sum_red_card(self):
        current_sum = 0
        card = self.env.deck.draw_color_card(color="red")
        self.assertTrue(self.env.evaluate_sum(current_sum, card) <= 0)

    def test_evaluate_sum_black_card(self):
        current_sum = 0
        card = self.env.deck.draw_color_card(color="black")
        self.assertTrue(self.env.evaluate_sum(current_sum, card) >= 0)    
    
    def test_step_action_stick(self):
        self.env.step(0)
        self.assertTrue(self.env.current_state==(10, 1))

    def test_step_action_hit(self):
        self.env.step(1)
        self.assertTrue(self.env.current_state != (10, 1))

    def test_reset(self):
        self.env.done = True
        self.env.reset()
        self.assertFalse(self.env.done)
    
    def test_evaluate_current_state_end_game(self):
        self.env.current_state = (1, 22)
        self.env.evaluate_current_state()
        self.assertTrue(self.env.done)

    def test_evaluate_current_state_continue_game(self):
        self.env.current_state = (3, 17)
        self.env.evaluate_current_state()
        self.assertFalse(self.env.done)

    def test_play_game(self): # play once version - form of one arm bandit
        action = 0
        reward, next_state, done = self.env.step(action)
        self.assertTrue(done)

if __name__ == '__main__':
    unittest.main()