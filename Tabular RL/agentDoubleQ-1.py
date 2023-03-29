import numpy as np


class Agent(object):  # Keep the class name!
    """The world's simplest agent!"""

    def __init__(self, state_space, action_space):
        self.action_space = action_space
        self.state_space = state_space
        self.Q1 = np.ones((state_space, action_space))
        self.Q2 = np.ones((state_space, action_space))
        self.learning_rate = 0.1
        self.discount = 0.95
        self.action = np.random.randint(0, action_space)
        self.state = 0
        self.epsilon = 0.05
        self.name = "Double Q-learning"

    def observe(self, observation, reward, done):
        future_q2 = self.Q2[observation, np.argmax(self.Q1[observation, :])]
        future_q1 = self.Q1[observation, np.argmax(self.Q2[observation, :])]
        if done and not reward:  # when we fall into a hole the observation is 0 so it doesn't get the right future q.
            future_q1 = 0
            future_q2 = 0

        if np.random.randint(0, 2):
            self.Q1[self.state, self.action] = self.Q1[self.state, self.action] + self.learning_rate * (
                reward + self.discount * future_q2 - self.Q1[self.state, self.action]
            )
        else:
            self.Q2[self.state, self.action] = self.Q2[self.state, self.action] + self.learning_rate * (
                reward + self.discount * future_q1 - self.Q2[self.state, self.action]
            )

    def act(self, observation):
        # Add your code here
        if np.random.random() <= self.epsilon:
            self.action = np.random.randint(0, self.action_space)
        else:
            Q_observation = self.Q1[observation, :] + self.Q2[observation, :]
            self.action = np.argmax(Q_observation)
        self.state = observation
        return self.action

    def reset(self):
        self.Q1 = np.ones((self.state_space, self.action_space))
        self.Q2 = np.ones((self.state_space, self.action_space))