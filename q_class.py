import os, json, random, ast, sys, numpy
from gameState import makeInitGameState
from encode2 import compress_and_encode
from redis_class import *
def stop():
    sys.exit()

class Bot:
    def __init__(self, name, alpha=0.15, gamma=0.95, epsilon=0.15):
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.name = name


    def choose_action(self, state_str, gameState):
        state_path = f"{self.name}:{state_str}"
        if not r.exists(state_path):
            actions = gameState.get_all_valid_moves()
            data = {}
            for action in actions:
                data[str(action)] = 0
            r.hset(state_path, mapping=data)
            return str(random.choice(actions))
        if random.random() < self.epsilon:
            actions = r.hkeys(state_path)
            return random.choice([f.decode('utf-8') for f in actions])
        else:
            max_value = max(r.hvals(state_path))
            max_keys = [key for key, value in r.hgetall(state_path).items() if value == max_value]
            return random.choice([f.decode('utf-8') for f in max_keys])
    def save_data(self):
        save_data(self.table_name, json.dumps(self.Q))



class Environment:
    def __init__(self, bot1, bot2):
        self.bot1 = bot1
        self.bot2 = bot2
        self.bots = {
            "red": self.bot1,
            "black": self.bot2,
            "white": None  # AI player
        }
        self.reset()
    def reset(self):
        self.gameState = makeInitGameState()
        self.limit_round = 60
        self.done = False
    def train(self, episodes=100):

        for i in range(episodes):
            print("Training: ",i)
            self.reset()
            while not self.done and self.limit_round:
                bot = self.bots[self.gameState.turn]
                state_str = compress_and_encode(str(self.gameState.pieces))
                action_str = bot.choose_action(state_str, self.gameState)
                action = ast.literal_eval(action_str)
                next_state, reward = self.perform_action(action) #type: gameState
                next_state_str = compress_and_encode(str(next_state.pieces))
                path = f"{bot.name}:{state_str}"
                nextpath = f"{bot.name}:{next_state_str}"
                if not r.exists(nextpath):
                    data = {}
                    next_actions = self.gameState.get_all_valid_moves()
                    for action in next_actions:
                        data[str(action)] = 0
                    r.hset(nextpath, mapping=data)
                
                old_value = float(r.hget(path, action_str).decode('utf-8'))
                values = r.hvals(nextpath)
                next_max = float(max([v.decode('utf-8') for v in values]))
                # print(f"{old_value} + {bot.alpha} * ({reward} + {bot.gamma} * {next_max} - {old_value})")
                # print(f"{type(old_value)} + {type(bot.alpha)} * ({type(reward)} + {type(bot.gamma)} * {type(next_max)} - {type(old_value)})")
                # stop()
                new_value = old_value + bot.alpha * (reward + bot.gamma * next_max - old_value)
                r.hset(path, action_str, new_value)          
                self.gameState = next_state
                self.limit_round -= 1

        r.close()
    def perform_action(self, action):
        self.gameState.move(action)
        reward = self.gameState.evaluate_board()
        # print("reward", reward)
        return self.gameState, reward
