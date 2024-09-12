from q_class import *

bot2 = Bot("black")
bot1 = Bot("red", 0.15, 0.95, 0.5)


env = Environment(bot1, bot2)
def train():
    try:
        env.train(1000)
    except Exception as e:
        print(e)
    finally:
        train()

train()