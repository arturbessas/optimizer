import json
from datetime import datetime
from pprint import pprint
import time
import os, psutil


class dotdict(dict):
    """dot.notation access to dictionary attributes"""

    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


class Candle:
    def __init__(self, date, close):
        self.date = date
        self.close = close
        self.averages = {}


class Setup:
    def __init__(self, avg, dx, tp, sl, p1, q1, p2, q2, p3, q3, p4, q4):
        self.avg = avg
        self.dx = dx
        self.tp = tp
        self.sl = sl
        self.increases = [(p1, q1), (p2, q2), (p3, q3), (p4, q4)]


def getData(year, month):
    inputFile = "dados/dados" + str(year) + str(month) + ".json"
    print(inputFile)
    with open(inputFile, "rb") as json_file:
        dados = json.load(json_file)
    print("sucesso!")
    return dotdict(dados)


def getCandles(data):
    candles = []
    i = 0
    # primeiro tick válido
    while datetime.strptime(data[i].d, "%Y-%m-%d %H:%M:%S").hour < 9:
        i += 1

    last_time = datetime.strptime(data[i].d, "%Y-%m-%d %H:%M:%S")
    last_close = data[i].p

    for tick in data:
        now = datetime.strptime(tick.d, "%Y-%m-%d %H:%M:%S")
        if now.hour < 9 or now.hour > 17:
            continue
        if not now.minute == last_time.minute:
            candles.append(Candle(last_time, last_close))
            last_time = now
            calculateAverages(candles)
        last_close = tick.p

    return dotdict(candles)


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
    return dotdict(params)


def getSetups(params):
    setups = []
    for media in range(params.avg_start, params.avg_end + 1, params.avg_step):
        for dx in range(params.dx_start, params.dx_end + 1, params.dx_step):
            for tp in range(params.tp_start, params.tp_end + 1, params.tp_step):
                for sl in range(params.sl_start, params.sl_end + 1, params.sl_step):
                    for p1 in range(params.p1_start, params.p1_end + 1, params.p1_step):
                        for q1 in range(
                            params.q1_start, params.q1_end + 1, params.q1_step
                        ):
                            if (p1 == 0 or q1 == 0) and not p1 == q1:
                                break

                            for p2 in range(
                                params.p2_start, params.p2_end + 1, params.p2_step
                            ):
                                if (p1 == 0 and not p2 == 0) or (
                                    p2 <= p1 and not p2 == 0
                                ):
                                    break

                                for q2 in range(
                                    params.q2_start, params.q2_end + 1, params.q2_step
                                ):
                                    if (p2 == 0 or q2 == 0) and not p2 == q2:
                                        break

                                    for p3 in range(
                                        params.p3_start,
                                        params.p3_end + 1,
                                        params.p3_step,
                                    ):
                                        if (p2 == 0 and not p3 == 0) or (
                                            p3 <= p2 and not p3 == 0
                                        ):
                                            break

                                        for q3 in range(
                                            params.q3_start,
                                            params.q3_end + 1,
                                            params.q3_step,
                                        ):
                                            if (p3 == 0 or q3 == 0) and not p3 == q3:
                                                break

                                            for p4 in range(
                                                params.p4_start,
                                                params.p4_end + 1,
                                                params.p4_step,
                                            ):
                                                if (p3 == 0 and not p4 == 0) or (
                                                    p4 <= p3 and not p4 == 0
                                                ):
                                                    break

                                                for q4 in range(
                                                    params.q4_start,
                                                    params.q4_end + 1,
                                                    params.q4_step,
                                                ):
                                                    if (
                                                        p4 == 0 or q4 == 0
                                                    ) and not p4 == q4:
                                                        break

                                                    setup = Setup(
                                                        media,
                                                        dx,
                                                        tp,
                                                        sl,
                                                        p1,
                                                        q1,
                                                        p2,
                                                        q2,
                                                        p3,
                                                        q3,
                                                        p4,
                                                        q4,
                                                    )

                                                    if validSetup(setup):
                                                        setups.append(setup)
                                                        if len(setups) % 1000 == 0:
                                                            print(len(setups))
                                                            print(setups[-256].__dict__)

                                                    # print(setup.__dict__)


def validSetup(setup):
    for (p, q) in setup.increases:
        if p >= setup.sl:
            return False

    return True


# start = time.time()
# dados = getData(2020, 12)
# print("Leitura de dados: " + str(time.time() - start) + "s")
# candles = getCandles(dados)
# print("Construção dos candles: " + str(time.time() - start) + "s")
# print(psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2)
# import pdb

# pdb.set_trace()
