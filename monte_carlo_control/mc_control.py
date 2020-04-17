import numpy as np
from easy21_environment.easy21 import *

def train_monte_carlo_control():
    # initialize the environment
    env = Easy21GameEnvironment()
    print(env.actions)
    print(env.state_space_max)
    
if __name__ == "__main__":
    train_monte_carlo_control()
