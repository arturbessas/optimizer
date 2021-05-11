import json
from datetime import datetime
import time
import os, psutil


class Candle:
    def __init__(self, date, close):
        self.date = date
        self.close = close
        self.averages = {}


def getData(year, month):
    inputFile = "dados/dados" + str(year) + str(month) + ".json"
    print(inputFile)
    with open(inputFile, "rb") as json_file:
        dados = json.load(json_file)
    print("sucesso!")
    return dados


def getCandles(data):
    candles = []
    i = 0
    # primeiro tick válido
    while datetime.strptime(data[i]["d"], "%Y-%m-%d %H:%M:%S").hour < 9:
        i += 1

    last_time = datetime.strptime(data[i]["d"], "%Y-%m-%d %H:%M:%S")
    last_close = data[i]["p"]

    for tick in data:
        now = datetime.strptime(tick["d"], "%Y-%m-%d %H:%M:%S")
        if now.hour < 9 or now.hour > 17:
            continue
        if not now.minute == last_time.minute:
            candles.append(Candle(last_time, last_close))
            last_time = now
            calculateAverages(candles)
        last_close = tick["p"]

    return candles


def calculateAverages(candles):
    for i in range(3, 30):
        getAverage(candles, i)


def getAverage(candles, i):
    if len(candles) <= i:
        candles[-1].averages[i] = sum(c.close for c in candles[:-1]) / len(candles)
    else:
        m = 2 / (i + 1)
        candles[-1].averages[i] = (
            candles[-1].close - candles[-2].averages[i]
        ) * m + candles[-2].averages[i]


def getParams():
    with open("params.json", "rb") as json_file:
        params = json.load(json_file)
    return params


# start = time.time()
# dados = getData(2020, 12)
# print("Leitura de dados: " + str(time.time() - start) + "s")
# candles = getCandles(dados)
# print("Construção dos candles: " + str(time.time() - start) + "s")
# print(psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2)
# import pdb

# pdb.set_trace()
