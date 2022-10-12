import requests
import pandas as pd
import numpy
url = 'https://www.nseindia.com/api/option-chain-indices?symbol=BANKNIFTY'
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Apple'
                              'WebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
                              'accept-language': 'en,gu;q=0.9,hi;q=0.8',
                              'accept-encoding': 'gzip, deflate, br'}
session = requests.Session()
requests = session.get(url, headers=headers)
cookies = dict(requests.cookies)
requests = session.get(url, headers=headers,cookies=cookies).json()

# print(requests)
df = pd.DataFrame(requests)
df1 = pd.DataFrame(df['filtered']['data']).fillna(0)
# print(df1)

def dataframe(df1):
    data = []
    for i in range(0,len(df1)):
        calloi = callcoi = cltp = putoi = putcoi = pltp = 0
        stp = df1['strikePrice'][i]

        if(df1['CE'][i]==0):
            calloi = callcoi = 0
        else:
            calloi = df1['CE'][i]['openInterest']
            callcoi = df1['CE'][i]['changeinOpenInterest']
            cltp = df1['CE'][i]['lastPrice']
            expdate = df1['CE'][i]["expiryDate"]
            underlying = df1['CE'][i]["underlyingValue"]
            diff = (stp - df1['CE'][i]["underlyingValue"])*(stp - df1['CE'][i]["underlyingValue"])
        if (df1['PE'][i] == 0):
            putoi = putcoi = 0
        else:
            putoi = df1['PE'][i]['openInterest']
            putcoi = df1['PE'][i]['changeinOpenInterest']
            pltp = df1['PE'][i]['lastPrice']

        opdata = {
            'CALLOI' : calloi, 'CALLCOI' : callcoi, 'CALL LTP' : cltp, 'STRIKE PRICE' : stp,
            'PUTOI': putoi, 'PUTCOI': putcoi, 'PUT LTP': pltp, 'EXP DATE' : expdate, 'UNDERLYING': underlying, 'diff': diff
        }
        data.append(opdata)
    optionchain = pd.DataFrame(data)
    return optionchain

optionchain = dataframe(df1)

for j in range(0, len(optionchain["CALL LTP"])):


    if optionchain["diff"][j] == optionchain["diff"].min():

        print("\nATM: (For Straddle)")
        print("CALL:", optionchain["CALL LTP"][j], "_________BANKNIFTY", optionchain["EXP DATE"][j][:-5],
              optionchain["STRIKE PRICE"][j], "CE", "__________Tot Val", 25 * optionchain["CALL LTP"][j])

        print("PUT:", optionchain["PUT LTP"][j], "_________BANKNIFTY", optionchain["EXP DATE"][j][:-5],
              optionchain["STRIKE PRICE"][j], "PE", "__________Tot Val", 25 * optionchain["PUT LTP"][j])
        print("Total:", 25 * optionchain["CALL LTP"][j]+25 * optionchain["PUT LTP"][j])

    if optionchain["CALL LTP"][j] > 80 and optionchain["CALL LTP"][j] < 120 :
        print("\nCALL OPTION")
        print("CALL(Premium 80 to 100):",optionchain["CALL LTP"][j],"_________BANKNIFTY",optionchain["EXP DATE"][j][:-5],optionchain["STRIKE PRICE"][j],"CE","__________Tot Val",25*optionchain["CALL LTP"][j])

    if optionchain["PUT LTP"][j] > 80 and optionchain["PUT LTP"][j] < 120 :
        print("\nPUT OPTION")
        print("PUT (Premium 80 to 100):",optionchain["PUT LTP"][j],"_________BANKNIFTY",optionchain["EXP DATE"][j][:-5],optionchain["STRIKE PRICE"][j],"PE","__________Tot Val",25*optionchain["PUT LTP"][j])

    if optionchain["PUTOI"][j] == optionchain["PUTOI"].max() :
        print("\nlARGEST OI - PUT OPTION :")
        print("PUT:",optionchain["PUT LTP"][j],"_________BANKNIFTY",optionchain["EXP DATE"][j][:-5],optionchain["STRIKE PRICE"][j],"PE","__________Tot Val",25*optionchain["PUT LTP"][j])

    if optionchain["CALLOI"][j] == optionchain["CALLOI"].max() :
        print("\nlARGEST OI - CALL OPTION :")
        print("CALL:", optionchain["CALL LTP"][j], "_________BANKNIFTY", optionchain["EXP DATE"][j][:-5],
              optionchain["STRIKE PRICE"][j], "CE", "__________Tot Val", 25 * optionchain["CALL LTP"][j])
