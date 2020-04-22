import numpy as np
from easy21_environment.easy21 import *
import matplotlib.pyplot as plt

def train_monte_carlo_control():
    # initialize the environment
    env = Easy21GameEnvironment()
    actions = env.actions
    state_space_dim = env.state_space_max

    # build a q_table : dictionary of the form ((state_x, state_y),action) : expected_value for all possible states
    state_space = {
            "a" : (0, state_space_dim[0]),
            "b" : (-3*state_space_dim[1], 3*state_space_dim[1])
    }
    action_space = {
        "min" : actions[0],
        "max" : actions[1]
    }
    q_table = build_q_table(state_space, action_space)
   
    # TODO: figure out how to compare policies from two q_tables

    # CONSTANTS
    EPISODES = 100000
    n_0 = 100
    lambda_rate = 1

    n_s_a = {} # N(s, a) - number of times an action is taken at a particular state
    n_s = {} # N(s) - number of times a state is visited

    # Game Summary
    won = 0
    lost = 0
    drawn = 0
    all_rewards = []
    avg_rewards = []

    for episode in range(EPISODES):
        state = env.current_state
        done = False
        time_step = 0

        returns = {}
        episode_memory = [] # (state, action, reward) list for each episode

        while not done:
            # increment state visit count
            time_step += 1
            if state in n_s.keys():
                n_s[state] += 1
            else:
                n_s[state] = 1
            
            # select action according to epsilon-greedy policy
            epsilon = n_0 / (n_0 + n_s[state])
            action = select_action_epsilon_greedy_policy(state, epsilon, q_table, actions)

            # increment action visit count
            if (state, action) in n_s_a.keys():
                n_s_a[(state, action)] += 1
            else:
                n_s_a[(state, action)] = 1
            
            # act in the environment
            reward, next_state, done = env.step(action)
            
            episode_memory.append((state, action, reward))
            
            
            if done:
                # do policy improvement
                # print("Episode {}. Episode memory length {}".format(episode, len(episode_memory)))
                for episode_i in range(len(episode_memory)):
                    state, action, reward = episode_memory[episode_i]
                    g = reward
                    for next_episode_i in range(episode_i+1, len(episode_memory)):
                        _, _, next_reward = episode_memory[next_episode_i]
                        g += next_reward
                    
                    q_table[(state, action)] = q_table[(state, action)] +  (1 / n_s_a[(state, action)]) * (g - q_table[(state, action)])
                   
                if reward == 1:
                    remarks = "Won"
                    won += 1
                elif reward == -1:
                    remarks = "Lost"
                    lost += 1
                else:
                    remarks = "Drawn"
                    drawn += 1

                all_rewards.append(reward)
                avg_reward = np.mean(all_rewards)
                avg_rewards.append(avg_reward)

                print("Episode {}: Reward is {} and game is {}".format(episode+1, reward, remarks))

                time_step = 0 # reset timestep counter
                env.reset()
                
                episode_memory = []
                break
            else:
                state = next_state

                # go to next timestep
                continue

    print("\n Summary: Won {}, Lost {}, Drawn {}".format(won, lost, drawn))    
    return q_table, avg_rewards

def select_action_epsilon_greedy_policy(state, epsilon, q_table, actions):
    # choose between random action and greedy action
    is_random = np.random.choice([True, False], p=[epsilon, 1-epsilon])
    if is_random:
         return np.random.choice(actions)
    else:
        max_reward = -100000
        selected_action = 0

        for action in actions:
            if max_reward < q_table[(state, action)]:
                max_reward = q_table[(state, action)]
                selected_action = action

        return selected_action
    

def build_q_table(state_space, action_space):
    """[Method that creates a q_table to represent the 
        expected reward of being in a certain state and doing a particular action]

    Arguments:
        \nstate_space {[dict]} -- [\n
            state_space = {
            "a" : (0, 2), // min and max bounds for the first element of the state tuple
            "b" : (0, 2), // min and max bounds for the second element of the state tuple
        }
        \n]
        \naction_space {[dict]} -- [\n
            action_space = {
            "min" : 0, // min action value possible
            "max" : 1 // max action value possible
        }
        \n]
    
    Returns:
        [dict] -- [q_table]
    """
    q_table = {}

    for action in action_space.values():
        for state_space_a in range(state_space["a"][0], state_space["a"][1]+1):
            for state_space_b in range(state_space["b"][0], state_space["b"][1]+1):
                q_table[((state_space_a, state_space_b), action)] = 0.0 #float("{:.2g}".format(np.random.normal(scale=0.1))) # initialize randomly

    return q_table


if __name__ == "__main__":
    q_table, avg_rewards = train_monte_carlo_control()
    
    #plt.scatter(range(len(avg_rewards)), avg_rewards, s=1)
    plt.plot(avg_rewards)
    plt.ylabel('AVERAGE REWARD')
    plt.xlabel("EPISODES")
    plt.title("Average reward at each episode")
    plt.show()

