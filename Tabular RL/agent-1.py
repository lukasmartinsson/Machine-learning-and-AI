import numpy as np


class Agent(object):  # Keep the class name!
    """The world's simplest agent!"""

    def __init__(self, state_space, action_space):
        self.action_space = action_space
        self.state_space = state_space
        self.Q = np.ones((state_space, action_space))
        self.learning_rate = 0.1
        self.discount = 0.95
        self.action = np.random.randint(0, action_space)
        self.state = 0
        self.epsilon = 0.05
        self.total_reward = 0
        self.name = "Q-learning"

    def observe(self, observation, reward, done):
        future_q = np.max(self.Q[observation, :])
        if done and not reward:  # when we fall into a hole the observation is 0 so it doesn't
            future_q = 0
        self.Q[self.state, self.action] = self.Q[self.state, self.action] + self.learning_rate * (
            reward + self.discount * future_q - self.Q[self.state, self.action]
        )

    def act(self, observation):
        # Add your code here
        if np.random.random() <= self.epsilon:
            self.action = np.random.randint(0, self.action_space)
        else:
            self.action = np.argmax(self.Q[observation, :])
        self.state = observation
        return self.action

    def reset(self):
        self.Q = np.ones((self.state_space, self.action_space))
