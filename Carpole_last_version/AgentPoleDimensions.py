#AGENTE ENTRENAMIENTO
from sklearn.preprocessing import KBinsDiscretizer
import numpy as np 
import matplotlib.pyplot as plt
import math
from typing import Tuple

# import gym 
import gym
env = gym.make('CartPole-v1')
ep_rewards = []
cumulative_reward = {'ep': [], 'avg': [], 'max': [], 'min': []}
show_every = 50
stats_every = 50
save_every = 50
episodes = 2000
max_learning_rate = 1.0
decrase_learning_rate_factor = 20
max_exploration_rate = 1.0
decrase_exploration_rate_factor = 20
decrease_learning_rate_step = 0.00001
decrease_exploration_rate_step = 0.00001
learning_rate_decreased = 1.0
exploration_rate_decreased = 1.0


n_bins = ( 6 , 12 )
lower_bounds = [ env.observation_space.low[2], -math.radians(50) ]
upper_bounds = [ env.observation_space.high[2], math.radians(50) ]

def get_discrete_state(cart_position, cart_velocity , angle, pole_velocity) -> Tuple[int,...]:
    est = KBinsDiscretizer(n_bins=n_bins, encode='ordinal', strategy='uniform')
    est.fit([lower_bounds, upper_bounds ])
    return tuple(map(int,est.transform([[angle, pole_velocity]])[0]))

Q = np.zeros(n_bins + (env.action_space.n,))

def policy( state : tuple ):
    return np.argmax(Q[state])

def new_Q_value( reward : float ,  new_state : tuple , discount_factor=1 ) -> float:
    """Utilizar descuento para los valores futuros"""
    value = np.max(Q[new_state])
    learned_value = reward + discount_factor * value
    return learned_value

def learning_rate(n : int , min_rate=0.01 ) -> float  :
    """Disminuye el aprendizaje conforme pasan los episodios (aprende mas al principio)"""
    return max(min_rate, min(max_learning_rate, max_learning_rate - math.log10((n + 1) / decrase_learning_rate_factor)))
    #return max(min_rate, min(max_learning_rate, learning_rate_decreased))
    return 1


def exploration_rate(n : int, min_rate= 0.1 ) -> float :
    """Disminuye la exploración conforme pasan los episodios (más episodios, menos exploración)"""
    return max(min_rate, min(max_exploration_rate, max_exploration_rate - math.log10((n  + 1) / decrase_exploration_rate_factor)))
    #return max(min_rate, min(max_exploration_rate, exploration_rate_decreased))
    

ever_finished = False
for episode in range(episodes):
    episode_reward = 0
    initial_state = env.reset()[0]
    current_state, done = get_discrete_state(initial_state[0], initial_state[1], initial_state[2], initial_state[3]), False
    if episode % save_every == 0:
        np.save(f"qtables/V5/{episode}-qtable.npy",Q)
    print(episode)
    """
    if episode % show_every == 0:
        print(episode)"""
    learning_rate_decreased -= decrease_learning_rate_step
    learning_rate_decreased -= decrease_exploration_rate_step
    truncated = False
    while not done and not truncated: 
        action = policy(current_state) # exploit    
        """Inserta una accion random"""
        if np.random.random() < exploration_rate(episode) : 
            action = env.action_space.sample() # explore 
        obs, reward, done, truncated, info = env.step(action)
        episode_reward += reward
        new_state = get_discrete_state(*obs)
        
        """Actualiza la tabla de Q"""
        gamma = learning_rate(episode)
        new_value = new_Q_value(reward , new_state)
        old_value = Q[current_state][action]
        Q[current_state][action] = (1-gamma)*old_value + gamma*new_value
        
        current_state = new_state
        if truncated:
            if not ever_finished:
                print("Llegó al final en el episodio ", episode)
                np.save(f"qtables/V5/{episode}-qtable.npy",Q)
                ever_finished = True
        ep_rewards.append(episode_reward)
        if not episode % stats_every:
            average_reward = sum(ep_rewards[-stats_every:])/stats_every
            cumulative_reward['ep'].append(episode)
            cumulative_reward['avg'].append(average_reward)
            cumulative_reward['max'].append(max(ep_rewards[-stats_every:]))
            cumulative_reward['min'].append(min(ep_rewards[-stats_every:]))

np.save(f"qtables/V5/{episode}-qtable.npy",Q) #Para Guardar el ultimo Q
"""Graficar los valores de performance obtenidos"""
plt.plot(cumulative_reward['ep'], cumulative_reward['avg'], label="average rewards")
plt.plot(cumulative_reward['ep'], cumulative_reward['max'], label="max rewards")
plt.plot(cumulative_reward['ep'], cumulative_reward['min'], label="min rewards")
plt.legend(loc=4)
plt.show()  

env.close()