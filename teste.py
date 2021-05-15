import random
import json
import sys
from datetime import datetime


random.seed()
steps = 0
up = 0
down = 0
price = 100.0

gain = 114
loss = 90
nGain = 0
nLoss = 0

ocurrences = 0


def fazData(dado):
    return datetime.strptime(dado["d"], "%Y-%m-%d %H:%M:%S")


class param:
    def __init__(self):
        pass


def main(args):
    teste = param()
    teste.doido = 1
    print(teste.doido)


def getPrice():
    global steps, price
    steps += 1
    passo = random.randint(1, 2)
    if passo == 1:
        price = price + 0.5
    elif passo == 2:
        price = price - 0.5
    return price


# while ocurrences < 1000:
#     getPrice()
#     if price == gain:
#         price = 100
#         nGain += 1
#         ocurrences += 1
#     elif price == loss:
#         price = 100
#         nLoss += 1
#         ocurrences += 1


# print(f"gains: {nGain} / losses: {nLoss}")

if __name__ == "__main__":
    main(sys.argv)
