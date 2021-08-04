import gym
import copy
import numpy as np
import matplotlib.pyplot as plt

import torch
import torch.nn as nn
import torch.optim as optim
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

from model.q_network import QNetwork, Trainer

env = gym.make('FrozenLake-v0')
policy = QNetwork(num_state=env.observation_space.n, num_action=env.action_space.n).to(device)

# Set learning parameters
num_epoch = 200
trainer = Trainer(policy)

episode_reward, episode_length = [], []
observation = env.reset()
env.render()
for epoch in range(num_epoch):
    state = env.reset()
    state = torch.tensor(state, device=device, dtype=torch.int16)

    episode_reward.append(0.0)
    episode_length.append(0)

    done = False
    while True:
        policy.train()
        action, prediction = policy(state)

        state_, reward, done, info = env.step(action.item())
        trainer.train(prediction, action, reward)

        episode_reward[-1] += reward
        episode_length[-1] += 1
        state = state_
        if done:
            print(f"[{epoch:04}] episode_reward: {episode_reward[-1]}, episode_length: {episode_length[-1]}")
            break
print(f"*** mean reward: {sum(episode_reward) / len(episode_reward)}, mean length: {sum(episode_length) / len(episode_reward)}")
for i in range(env.observation_space.n):
    print(policy(i)[1].tolist())
env.close()