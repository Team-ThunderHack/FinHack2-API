import pandas as pd
import json
import time
import datetime
import calendar
from datetime import date
from threading import Timer
from datetime import date,timedelta
from breeze_connect import BreezeConnect
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import warnings
warnings.simplefilter("ignore")

@api_view(['GET'])
def nifty(request):
    today = date.today()
    back5days = today + timedelta(days=-5, hours=0)
    tomorrow = today + timedelta(days=1, hours=0)

    d = date.today()
    x = calendar.day_name[d.weekday()]
    if(x=="Saturday" or x=="Sunday"):
        return (json.dumps([-2,0,0,0,0,0]))
    
    breeze = BreezeConnect(api_key="")
    breeze.generate_session(api_secret="", 
                            session_token="")

    iso_date_string = datetime.datetime.strptime("21/03/2022","%d/%m/%Y").isoformat()[:10] + 'T05:30:00.000Z'
    iso_date_time_string = datetime.datetime.strptime("21/03/2022 23:59:59","%d/%m/%Y %H:%M:%S").isoformat()[:19] + '.000Z'

    historicalData = breeze.get_historical_data(interval="1day",
                        from_date= str(back5days) + "T07:00:00.000Z",
                        to_date= str(today) + "T07:00:00.000Z",
                        stock_code="NIFTY",
                        exchange_code="NSE",
                        product_type="",
                        expiry_date="",
                        right="",
                        strike_price="")
    lengthOfList = (len(historicalData['Success']))
    latestDay = historicalData['Success'][lengthOfList-1]

    previousDayLowPrice = latestDay['low']
    previousDayHighPrice = latestDay['high']

    breeze.ws_connect()

    lastPrice = 0 
    openPrice = 0

    def on_ticks(ticks):
        global lastPrice
        global openPrice
        lastPrice = ticks['last']
        openPrice = ticks['open']

    breeze.on_ticks = on_ticks
    df = breeze.subscribe_feeds(exchange_code="NSE", 
                        stock_code="NIFTY", 
                        product_type="", 
                        expiry_date="", 
                        strike_price="", right="", 
                        get_exchange_quotes=True, 
                        get_market_depth=False)
    time.sleep(1.1)

    breeze.unsubscribe_feeds(exchange_code="NSE", 
                        stock_code="NIFTY", 
                        product_type="", 
                        expiry_date="", 
                        strike_price="", right="", 
                        get_exchange_quotes=True, 
                        get_market_depth=False)
    breeze.ws_disconnect()

    check = 0

    if(float(openPrice) < float(previousDayHighPrice) and float(openPrice) > float(previousDayLowPrice) and 
        float(lastPrice) > float(previousDayHighPrice)):
            check=1
    if(float(openPrice) < float(previousDayHighPrice) and float(openPrice) > float(previousDayLowPrice) and 
    float(lastPrice) < float(previousDayLowPrice)):
        check=-1

    resultJSON = []

    if(check==1):
        resultJSON = [check , previousDayLowPrice , previousDayHighPrice , 
                    lastPrice , openPrice , (lastPrice/100)*100]
    else:
        resultJSON = [check , previousDayLowPrice , previousDayHighPrice , 
                    lastPrice , openPrice , ((lastPrice/100)*100)+100]

    return  Response(json.dumps(resultJSON))

@api_view(['GET'])
def previousRecommendations(request):
    today = date.today()
    back10days = today + timedelta(days=-10, hours=0)
    tomorrow = today + timedelta(days=1, hours=0)

    breeze = BreezeConnect(api_key="8%@92h9*115gI3u022K37f=G&236B893")
    breeze.generate_session(api_secret="2t(52wI22380C482DBl%85q1Q7834t2J", 
                            session_token="2125876")

    historicalData = breeze.get_historical_data(interval="1day",
                            from_date= str(back10days) + "T07:00:00.000Z",
                            to_date= str(today) + "T07:00:00.000Z",
                            stock_code="NIFTY",
                            exchange_code="NSE",
                            product_type="cash",
                            expiry_date="",
                            right="",
                            strike_price="")
    data = (historicalData['Success'])
    length = len(data)
    marketData = []
    for entries in data:
        openPrice = entries['open']
        dateOfentry = entries['datetime']
        highPrice = entries['high']
        lowPrice = entries['low']
        closePrice = entries['close']
        marketData.append([openPrice,dateOfentry[0:10],highPrice,lowPrice,closePrice])

    pastRecomendations = []
    for i in range(1,length):
        if(marketData[i][0]>marketData[i-1][3] and 
           marketData[i][0]<marketData[i-1][2] and
           marketData[i][2]>marketData[i-1][2]):
            price = (int(int(float(marketData[i-1][2]))/100))*100
            pastRecomendations.append([(marketData[i][1]),price,"PE"])

        if(marketData[i][0]>marketData[i-1][3] and 
           marketData[i][0]<marketData[i-1][2] and
           marketData[i][3]<marketData[i-1][3]):
            price = ((int(int(float(marketData[i-1][3]))/100))*100)+100
            pastRecomendations.append([(marketData[i][1]),price,"CE"])

    return  Response(json.dumps(pastRecomendations))