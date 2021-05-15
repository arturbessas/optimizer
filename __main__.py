from dataLoader import *
from pprint import pprint
import time


def main():
    ini = time.time()
    params = getParams()
    setups = getSetups(params)
    print(time.time() - ini)
    input()
    for year in range(params.initial_year, params.final_year + 1):
        for month in range(1, 13):
            if (year == params.initial_year and month < params.initial_month) or (
                year == params.final_year and month > params.final_month
            ):
                continue

            dados = getData(year, month)
            candles = getCandles(dados)


if __name__ == "__main__":
    main()
