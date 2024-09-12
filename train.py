
import os, sys
import numpy as np
import pandas as pd

import random
def stop():
    sys.exit()

def make_actions():
    actions = []
    ratios = [4]#fix
    numbers = [i for i in range(100)]
    for ratio in ratios:
        for number in numbers:
            actions.append(f"{ratio}_{number}")
    return actions

def arrToState(arr):
    #mode, phuongsai, dolechchuan,...
    db = arr[0]
    mean = np.mean(arr)
    median = np.median(arr)
    # mode = stats.mode(arr)
    return f"{int(mean)}_{int(median)}"

def make_states(numpyArray):
    states = []
    for arr in numpyArray:
        state = arrToState(arr)
        if state not in states:  # Kiểm tra trùng lặp
            states.append(state)
    return states

class Env:
    def __init__(self):
        self.reset()
    def reset(self):
        self.maxPoint = 10
        self.minPoint = -10
        self.point = 0
        self.count = 0
    def step(self,action,result):
        if not action:
            return 0, False
        [ratio, number] = action.split("_")
        ratio = int(ratio)
        number = int(number)
        reward = -1
        # if ratio == 100:
        #     if number == result[0]:
        #         reward = ratio
        #     else:
        #         reward = -1
        # else:
        #     count = np.sum(result==number)
        #     if count  == 0:
        #         reward = -1
        #     else:
        #         reward = count*ratio
        count = np.sum(result==number)
        if count>0:
            reward = count*4
        self.point += reward
        self.count+=1
        if self.count ==4:
            return self.point, True
        return 0, False
        # if self.point>self.maxPoint:
        #     return self.maxPoint, True
        # elif self.point<self.minPoint:
        #     return self.minPoint, True
        # return 0, False

class X25Agent:
    def __init__(self, env, alpha=0.15, gamma=0.95, epsilon=0.15):
            self.env = env
            self.alpha = alpha  # Tốc độ học tập
            self.gamma = gamma  # Hệ số giảm dần
            self.epsilon = epsilon  # Xác suất chọn hành động ngẫu nhiên
            self.numpyData = readDataL2("dataTrain.csv")
            # print(self.numpyData)
            # print(self.numpyData.shape)
            # stop()
            self.actions = make_actions()
            self.states = make_states(self.numpyData)
            if os.path.exists('q_table.csv'):
                self.Q = pd.read_csv('q_table.csv',index_col=0).astype(float)
            else:
                self.Q = pd.DataFrame(0, index=self.states, columns=self.actions).astype(float)
    def choose_action(self,state):
            if state not in self.Q.index:
                return None
            if random.uniform(0, 1) < self.epsilon:
                return random.choice(self.actions)  
            else:
                actions = []
                max_value = self.Q.loc[state].max()
                for action in self.actions:
                    if self.Q.loc[state, action] == max_value:
                        actions.append(action)
                return random.choice(actions)

    def train(self, num_episodes):
        for episode in range(num_episodes):
            print("episode:", episode)
            self.env.reset()
            player = self.env
            done = False
            index = random.randint(0, len(self.numpyData)-10)
            state = arrToState(self.numpyData[index])
            while not done:
                action = self.choose_action(state)
                reward, done = self.env.step(action, self.numpyData[index+1])
                # print(state, action, reward, done)
                # print(reward, done)
                # stop()
                index+=1
                if index>= len(self.numpyData)-1:
                    break
                next_state = arrToState(self.numpyData[index])
                # Cập nhật giá trị Q
                old_value = self.Q.loc[state, action]
                next_max = self.Q.loc[state].max()
                self.Q.loc[state, action] = (1 - self.alpha) * old_value + self.alpha * (reward + self.gamma * next_max)
                state = next_state
            # break
        # Lưu ma trận Q vào file
        self.Q.to_csv('q_table.csv',index=True)
def load_q_table():
    return pd.read_csv('q_table.csv',index_col=0).astype(float)