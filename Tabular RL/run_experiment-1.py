import argparse
import gym
import importlib.util
import matplotlib.pyplot as plt
import numpy as np

np.set_printoptions(suppress=True)

parser = argparse.ArgumentParser()
parser.add_argument("--agentfile", type=str, help="file with Agent object", default="agentDoubleQ.py")
parser.add_argument("--env", type=str, help="Environment", default="FrozenLake-v1")
args = parser.parse_args()

spec = importlib.util.spec_from_file_location("Agent", args.agentfile)
agentfile = importlib.util.module_from_spec(spec)
spec.loader.exec_module(agentfile)
reward_list = []

try:
    env = gym.make(args.env, is_slippery=True)
    print("Loaded ", args.env)
except:
    print(args.env + ":Env")
    gym.envs.register(
        id=args.env + "-v0",
        entry_point=args.env + ":Env",
    )
    env = gym.make(args.env + "-v0")
    print("Loaded", args.env)

action_dim = env.action_space.n
state_dim = env.observation_space.n

action_dim = env.action_space.n
state_dim = env.observation_space.n

agent = agentfile.Agent(state_dim, action_dim)
runs = 5
episodes = 5000
timesteps = 100

total_reward = []

for run in range(runs):

    accumulated_reward = np.zeros(episodes)

    agent.reset()
    for episode in range(episodes):
        observation = env.reset()
        agent.state = 0
        agent.action = np.random.randint(0, action_dim)

        for t in range(timesteps):
            # env.render()
            action = agent.act(observation)
            observation, reward, done, info = env.step(action)
            agent.observe(observation, reward, done)

            if done:
                accumulated_reward[episode] = reward
                break

    try:
        print("Q1", agent.Q1)
        print("Q2", agent.Q2)
    except:
        print("Q", agent.Q)

    total_reward.append(accumulated_reward)

env.close()


ci = 0.95 * (np.std(total_reward, axis=0)) / np.sqrt(len(total_reward))

total_mean_reward = np.mean(total_reward, axis=0)

agg_episodes = 20
agg__mean_reward = [
    sum(total_mean_reward[i : i + agg_episodes]) / agg_episodes for i in range(0, len(total_mean_reward), agg_episodes)
]
total_mod = []
for agg in range(len(agg__mean_reward)):
    for _ in range(agg_episodes):
        total_mod.append(agg__mean_reward[agg])

ci_mean = [sum(ci[i : i + agg_episodes]) / agg_episodes for i in range(0, len(ci), agg_episodes)]
total_ci_mod = []
for agg in range(len(ci_mean)):
    for _ in range(agg_episodes):
        total_ci_mod.append(ci_mean[agg])

x = np.array(total_mod)
c = np.array(total_ci_mod)

plt.plot(range(int(episodes)), total_mod, label="Moving average")
plt.fill_between(range(int(episodes)), (x - ci), (x + ci), color="teal", alpha=0.5, label="95% confidence interval")
plt.xlabel("Episodes")
plt.legend(loc="lower right")

plt.ylabel(f"Reward (avg over {agg_episodes})")
plt.title(f"{agent.name} plot")
plt.show()