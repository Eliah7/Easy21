import unittest
from monte_carlo_control.mc_control import *

class MonteCarloTest(unittest.TestCase):
    def setUp(self):
        pass

    def test_build_q_table_1_dimension(self):
        expected_q_table = {
            ((0,0),0) : 0,
            ((0,1),0) : 0,
            ((1,0),0) : 0,
            ((1,1),0) : 0,
            ((0,0),1) : 0,
            ((0,1),1) : 0,
            ((1,0),1) : 0,
            ((1,1),1) : 0,    
        }

        state_space = {
            "a" : (0, 1),
            "b" : (0, 1)
        }

        action_space = {
            "min" : 0,
            "max" : 1
        }

        q_table = build_q_table(state_space, action_space)
        self.assertEqual(expected_q_table.keys(), q_table.keys())

    def test_build_q_table_2_dimensions(self):
        expected_q_table = {
            ((0,0),0) : 0,
            ((0,1),0) : 0,
            ((0,2),0) : 0,
            ((1,0),0) : 0,
            ((1,1),0) : 0,
            ((1,2),0) : 0,
            ((2,0),0) : 0,
            ((2,1),0) : 0,
            ((2,2),0) : 0,
            ((0,0),1) : 0,
            ((0,1),1) : 0,
            ((0,2),1) : 0,
            ((1,0),1) : 0,
            ((1,1),1) : 0,
            ((1,2),1) : 0,
            ((2,0),1) : 0,
            ((2,1),1) : 0,
            ((2,2),1) : 0,
        }

        state_space = {
            "a" : (0, 2),
            "b" : (0, 2)
        }

        action_space = {
            "min" : 0,
            "max" : 1
        }

        q_table = build_q_table(state_space, action_space)
        self.assertEqual(expected_q_table.keys(), q_table.keys())

    def test_select_action_epsilon_greedy_policy_two(self):
        env = Easy21GameEnvironment()
        state_space = {
            "a" : (0, 1),
            "b" : (0, 1)
        }
        action_space = {
            "min" : 0,
            "max" : 1
        }
        q_table = build_q_table(state_space, action_space)
        
        epsilon = 0
        state = (0, 1)
        q_table[(state, 0)] = 40.0

        action = select_action_epsilon_greedy_policy(state, epsilon, q_table, env.actions)
        self.assertIsNotNone(action)
        self.assertTrue(action in [0, 1])
        self.assertEqual(action, 0)
    
    def test_select_action_epsilon_greedy_policy_two(self):
        env = Easy21GameEnvironment()
        state_space = {
            "a" : (0, 1),
            "b" : (0, 1)
        }
        action_space = {
            "min" : 0,
            "max" : 1
        }
        q_table = build_q_table(state_space, action_space)
        
        epsilon = 0
        state = (0, 1)
        q_table[(state, 1)] = 40.0

        action = select_action_epsilon_greedy_policy(state, epsilon, q_table, env.actions)
        self.assertIsNotNone(action)
        self.assertTrue(action in [0, 1])
        self.assertEqual(action, 1)
        

if __name__ == '__main__':
    unittest.main()