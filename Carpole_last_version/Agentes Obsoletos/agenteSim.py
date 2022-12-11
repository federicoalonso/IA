import numpy as np 
import gym
import sys
import time
env = gym.make('CartPole-v1')

q_table = np.load('5600000-qtable.npy')


discrete_buckets = [10]
bucket_amount = 10
#q_table = np.random.uniform(0, 0.5, (bucket_amount, bucket_amount, bucket_amount, bucket_amount, env.action_space.n))
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

for episode in range(10):
    episodeReward = 0

    discrete_state = get_discrete_state(env.reset()[0]) 
    done = False
    while not done:
        
        action = np.argmax(q_table[discrete_state])
        #print(discrete_state)
        print("Accion tomada ", action)
        print("Qtable en el estado discreto ", q_table[discrete_state])
        #print(action)
        obs, reward, done, info, _ = env.step(action)
        episodeReward += reward
        #print(obs)
        #env.render()
        time.sleep(0.05)
        if done:
            env.reset()

    print("Reward Total en episodio ", episode, ": ", episodeReward)

env.close()
