from teste import *

periodicity_1 = 0
periodicity_5 = 1
periodicity_10 = 2
periodicity_15 = 3
periodicity_30 = 4
periodicity_60 = 5

def calculateCandles(data):
    candles = {}
    periodicities = [1, 5, 10, 15, 30, 60]
    for t in periodicities:
        candles[t] = []
    lastTime = fazData(data[0])
    for i in range(len(data)):
        currentTime = fazData(data[i])
        if(not currentTime.minute == lastTime.minute):
            for j in perio


    

def main():
