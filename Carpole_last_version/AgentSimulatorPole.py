#AGENTE ENTRENAMIENTO
from sklearn.preprocessing import KBinsDiscretizer
import numpy as np 
import math
from typing import Tuple

# import gym 
import gym
env = gym.make('CartPole-v1', render_mode='human')

n_bins = ( 6 , 12 )
lower_bounds = [ env.observation_space.low[2], -math.radians(50) ]
upper_bounds = [ env.observation_space.high[2], math.radians(50) ]

def get_discrete_state( _ , __ , angle, pole_velocity ) -> Tuple[int,...]:
    """Convert continues state intro a discrete state"""
    est = KBinsDiscretizer(n_bins=n_bins, encode='ordinal', strategy='uniform')
    est.fit([lower_bounds, upper_bounds ])
    return tuple(map(int,est.transform([[angle, pole_velocity]])[0]))

#Carga la QTable a utilizar
Q = np.load('137-qtable.npy')


def policy( state : tuple ):
    return np.argmax(Q[state])

episodes = 5
sum_rewards = 0
won_qty = 0
for e in range(episodes):
    truncated = False
    notify = True
    rewards = 0
    initial_state = env.reset()[0]
    current_state, done = get_discrete_state(initial_state[0], initial_state[1], initial_state[2], initial_state[3]), False
    while not done and not truncated:
        action = policy(current_state)
        obs, reward, done, truncated, info = env.step(action)
        rewards += reward
        new_state = get_discrete_state(*obs)        
        current_state = new_state
        env.render()
        if truncated and notify:
            print("GANO!!!")
            notify = False
            won_qty += 1
    print("Episodio: ", e, " Reward obtenido: ", rewards)
    sum_rewards += rewards
    avg = sum_rewards/episodes
won_avg = sum_rewards/episodes
won_percentage = won_qty / episodes * 100
print("Porcentaje de ganados: ", won_percentage)
print("Promedio de rewards: ", avg)
print("Se ganaron: ", won_qty, " veces!")
print("Promedio de rewards obtenidos ", won_avg)
env.close()
            