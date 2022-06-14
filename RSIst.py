from time import sleep
import numpy
import Prices as db
import talib

inPosision = False

def rsivalue(firstAddress, SecoundAddress, key):
    global inPosision 
    rsiPeriod = 14
    rsiOverBought = 70
    rsiOverSoled = 30

    while True:
        closes = db.database(firstAddress, SecoundAddress, key).copy()
        print(len(closes))
        if len(closes) > rsiPeriod:
            np_closes = numpy.array(closes)
            rsi = talib.RSI(np_closes, rsiPeriod)
            print("the RSI value is: ", rsi)
            lastRsi = rsi[-1]
            print("the current rsi is{}".format(lastRsi))
            if lastRsi >= rsiOverBought:
                if inPosision == False:
                    print("sell! sell! sell!")
                    inPosision = True
                    return False                  
                else:
                    print("We already soled!")               
            elif lastRsi < rsiOverSoled:
                if inPosision == False:
                    print("We already bought")
                else:
                    print("buy! buy! buy!")
                    inPosision = False
                    return True
        sleep(10)


