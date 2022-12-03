import pandas as pd
import json
import time
import datetime
from threading import Timer
from datetime import date,timedelta
from breeze_connect import BreezeConnect
from rest_framework.decorators import api_view
import warnings
warnings.simplefilter("ignore")




@api_view(['GET'])
def nifty(request):
    today = date.today()
    back5days = today + timedelta(days=-5, hours=0)
    tomorrow = today + timedelta(days=1, hours=0)

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

    return (json.dumps(resultJSON))









@api_view(['GET'])
def banknifty(request):
    today = date.today()
    back5days = today + timedelta(days=-5, hours=0)
    tomorrow = today + timedelta(days=1, hours=0)

    breeze = BreezeConnect(api_key="")
    breeze.generate_session(api_secret="", 
                            session_token="")

    iso_date_string = datetime.datetime.strptime("21/03/2022","%d/%m/%Y").isoformat()[:10] + 'T05:30:00.000Z'
    iso_date_time_string = datetime.datetime.strptime("21/03/2022 23:59:59","%d/%m/%Y %H:%M:%S").isoformat()[:19] + '.000Z'

    historicalData = breeze.get_historical_data(interval="1day",
                        from_date= str(back5days) + "T07:00:00.000Z",
                        to_date= str(today) + "T07:00:00.000Z",
                        stock_code="BANKNIFTY",
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
                        stock_code="BANKNIFTY", 
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

    return (json.dumps(resultJSON))








@api_view(['GET'])
def previousnifty(request):
    ans=[]
    return (json.dumps(ans))









@api_view(['GET'])
def banknifty(request):
    ans=[]
    return (json.dumps(ans))