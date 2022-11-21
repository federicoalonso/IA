import gym
import numpy as np

env = gym.make('CartPole-v1', render_mode='human')

def epsilon_greedy_policy(state, Q, epsilon=0.1):
    explore = np.random.binomial(1, epsilon)
    if explore:
        action = env.action_space.sample()
        print('explore')
    else:
        action = np.argmax(Q[state])
        print('exploit')
    return action

def optimal_policy(state, Q):
    action = np.argmax(Q[state])
    return action

bins = np.linspace(-0.000001, 100., 2)
bins

def get_state(obs):
    d = np.digitize(obs, bins)
    state = tuple(d)
    return state

state = get_state(np.array([-1.4, -2., 0.23, 1.2]))
state

Q = np.random.random((2,2,2,2,2))
Q

obs, _ = env.reset()
print(obs)
done = False
while not done:
    state = get_state(obs)
    action = epsilon_greedy_policy(state, Q, 0.5)
    obs, reward, done, info, _ = env.step(action)
    print('->', state, action, reward, obs, done, info)
# env.close()