import numpy as np 
import gym
import matplotlib.pyplot as plt
import sys

LEARNING_RATE = 0.1
DISCOUNT = 0.85 #Reward futuros vs rewards actuales, mide cuanto nos interesa lo futuro y lo actual
episodes = 10000000
show_every = 100000
# Exploration settings
STATS_EVERY = 100000
save_every = 100000

# Para llevar un conteo y poder graficar
ep_rewards = []
aggr_ep_rewards = {'ep': [], 'avg': [], 'max': [], 'min': []}

env = gym.make('CartPole-v1')

discrete_buckets = [10]
bucket_amount = 10
q_table = np.random.uniform(0, 0, (bucket_amount, bucket_amount, bucket_amount, bucket_amount, env.action_space.n))
angle_min = -0.418
angle_max = 0.418 
velocity_min = -sys.maxsize
velocity_max = sys.maxsize
angular_vel_min = -sys.maxsize
angular_vel_max = sys.maxsize
position_min = -4.8
position_max = 4.8
bins_angle = np.linspace(angle_min, angle_max, bucket_amount)
bins_angular_velocity = np.linspace(angular_vel_min, angular_vel_max, bucket_amount)
bins_position = np.linspace(position_min, position_max, bucket_amount)
bins_velocity = np.linspace(velocity_min, velocity_max, bucket_amount)


def get_discrete_state(state):
    cart_position = state[0]
    cart_velocity =  state[1]
    pole_ang = state[2]
    pole_vel = state[3]
    discrete_position = np.digitize(cart_position, bins_position)
    discrete_velocity = np.digitize(cart_velocity, bins_velocity)
    discrete_angle = np.digitize(pole_ang, bins_angle)
    discrete_angular_velocity = np.digitize(pole_vel, bins_angular_velocity)
    discretized_state = (discrete_position, discrete_velocity, discrete_angle, discrete_angular_velocity)
    return discretized_state

discrete_state = get_discrete_state(env.reset()[0])


def epsilon_greedy_policy(state, Q, epsilon=0.1):
    explore = np.random.binomial(1, epsilon)
    if explore:
        action = env.action_space.sample()
        #print('explore')
    else:
        action = np.argmax(Q[state])
        #print('exploit')
    return action

def optimal_policy(state, Q):
    action = np.argmax(Q[state])
    return action
episode = 0

for episode in range(episodes):
    episode_reward = 0
    if episode % save_every == 0:
        np.save(f"qtables/{episode}-qtable.npy",q_table)
        print(episode)
    env.reset()
    terminated = False
    truncated = False
    if episode % show_every == 0:
        render = True
        #print(episode)
    else:
        render = False
    while not terminated and not truncated:
        action = epsilon_greedy_policy(discrete_state, q_table, 0.5)
        new_state, reward, terminated, truncated, info = env.step(action)
        episode_reward += reward
        new_discrete_state = get_discrete_state(new_state)
        #if render:
            #env.render()
        if not terminated:
            max_future_q = np.max(q_table[new_discrete_state])
            current_q = q_table[discrete_state + (action, )]
            new_q = (1 - LEARNING_RATE) * current_q + LEARNING_RATE * (reward + DISCOUNT * max_future_q)
            #print("q table antes ", q_table[discrete_state + (action, )])
            q_table[discrete_state + (action, )] = new_q
            #print("Nuevo Q: ", new_q)
            #print("q table actualizada ", q_table[discrete_state + (action, )])
        if truncated:
            print("Llegó al final en el episodio ", episode)
        
        discrete_state = new_discrete_state
    #print("Reward total obtenido: ", episode_reward)
    ep_rewards.append(episode_reward)
    if not episode % STATS_EVERY:
        average_reward = sum(ep_rewards[-STATS_EVERY:])/STATS_EVERY
        aggr_ep_rewards['ep'].append(episode)
        aggr_ep_rewards['avg'].append(average_reward)
        aggr_ep_rewards['max'].append(max(ep_rewards[-STATS_EVERY:]))
        aggr_ep_rewards['min'].append(min(ep_rewards[-STATS_EVERY:]))
        #print(f'Episode: {episode:>5d}, average reward: {average_reward:>4.1f}, current epsilon: {epsilon:>1.2f}')

np.save(f"qtables/{episode}-qtable.npy",q_table) #Guarda la ultima qtable generada
#Grafico de la ejecucion
plt.plot(aggr_ep_rewards['ep'], aggr_ep_rewards['avg'], label="average rewards")
plt.plot(aggr_ep_rewards['ep'], aggr_ep_rewards['max'], label="max rewards")
plt.plot(aggr_ep_rewards['ep'], aggr_ep_rewards['min'], label="min rewards")
plt.legend(loc=4)
plt.show()  

env.close()