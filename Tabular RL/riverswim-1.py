import gym
from gym import spaces
from gym.utils import seeding
import numpy as np


class Env(gym.Env):
    def __init__(self, n=6, small=5 / 1000, large=1):
        self.n = n
        self.small = small  # payout for 'backwards' action
        self.large = large  # payout at end of chain for 'forwards' action
        self.state = 0  # Start at beginning of the chain
        self.action_space = spaces.Discrete(2)
        self.observation_space = spaces.Discrete(self.n)

    def step(self, action):
        assert self.action_space.contains(action)

        reward = 0

        if action == 0:  # Go left
            if self.state == 0:
                reward = self.small
                done = True
                self.state = 0
                return self.state, reward, done, {}
            else:
                self.state -= 1
        else:
            if self.state == 0:  # 'forwards': go up along the chain
                self.state = np.random.choice([self.state, self.state + 1], p=[0.4, 0.6])
            elif self.state < self.n - 1:  # 'forwards': go up along the chain
                self.state = np.random.choice([self.state - 1, self.state, self.state + 1], p=[0.05, 0.6, 0.35])
            else:
                self.state = np.random.choice([self.state - 1, self.state], p=[0.4, 0.6])
                if self.state == self.n - 1:
                    done = True
                    reward = self.large
                    self.state = 0
                    return self.state, reward, done, {}
        done = False
        return self.state, reward, done, {}

    def reset(self):
        self.state = 0
        return self.state