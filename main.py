import requests
import json
company_list = []
json_data = {}
i = 0
#get 8645 companies' list
def get_symbols():
   r = requests.get('https://api.iextrading.com/1.0/ref-data/symbols')
   json_file = json.loads(r.text)
   symbols = [j['symbol'].lower() for j in json_file]
   return symbols

company_list = get_symbols()

#stocks
stock_type = ['book','chart','delayed-quote','dividends','logo','news','peers','quote','relevant','volume-by-venue']
for type in stock_type:
    i = 0
    while i < len(company_list):
        com_list = company_list[i:i+100] if i+100 <= len(company_list) else company_list[i:]
        com_str = ','.join(com_list)
        try:
            r_k = requests.get('https://api.iextrading.com/1.0/stock/market/batch?symbols='+com_str+'&types='+type)
        except:
            continue
        json_data = json.loads(r_k.text)
        json_data.update(json_data)
        i += 100
    with open('../datasets/stocks/'+type+'.json', 'w') as outf:
        json.dump(json_data, outf)
#stocks-list
list_type = ['mostactive','gainers','losers','iexvolume','iexpercent']
for type in list_type:
    try:
        r_k = requests.get('https://api.iextrading.com/1.0/stock/market/list/'+type)
    except:
        continue
    json_data = json.loads(r_k.text)
    with open('../datasets/stocks/'+'list_'+type+'.json', 'w') as outf:
        json.dump(json_data, outf)

#reference data
ref_type = ['symbols','symbol-directory']
for type in ref_type:
    r_k = requests.get('https://api.iextrading.com/1.0/ref-data/'+type)
    with open('../datasets/ref_data/'+type+'.txt', 'w') as outf:
        outf.write(r_k.text)


#IEX market data
r_l = requests.get('https://api.iextrading.com/1.0/tops/last')
json_data = json.loads(r_l.text)
with open('../datasets/market_data/tops_last.json', 'w') as outf:
    json.dump(json_data, outf)

json_data = {}
#IEX market data-deep
for company in com_list:
    try:
        r_k = requests.get('https://api.iextrading.com/1.0/deep?symbols='+company)
    except:
        continue
    json_data = json.loads(r_k.text)
    json_data.update(json_data)
with open('../datasets/market_data/deeps.json', 'w') as outf:
    json.dump(json_data, outf)

#IEX stats
stats_type = ['intraday','records']
for type in stats_type:
    r_k = requests.get('https://api.iextrading.com/1.0/stats/'+type)
    json_data = json.loads(r_k.text)
    with open('../datasets/stats_data/'+type+'.json', 'w') as outf:
        json.dump(json_data, outf)


#IEX stats historical
r_h = requests.get('https://api.iextrading.com/1.0/stats/historical')
with open('../datasets/stats_data/historical.txt', 'w') as outf:
    outf.write(r_h.text)

 
# 5-year stock price data
while i < len(company_list):
    com_list = company_list[i:i+50] if i+50 <= len(company_list) else company_list[i:]
    com_str = ','.join(com_list)
    try:
        r_ = requests.get('https://api.iextrading.com/1.0/stock/market/batch?symbols='+com_str+'&types=chart&range=5y')
    except:
        continue
    json_data = json.loads(r_.text)
    json_data.update(json_data)
    i += 50
with open('../datasets/stocks/chart_5y.json', 'w') as outf:
    json.dump(json_data, outf)

#5-year dividends data
while i < len(company_list):
    com_list = company_list[i:i+50] if i+50 <= len(company_list) else company_list[i:]
    com_str = ','.join(com_list)
    try:
        r_ = requests.get('https://api.iextrading.com/1.0/stock/market/batch?symbols='+com_str+'&types=dividends&range=5y')
    except:
        continue
    json_data = json.loads(r_.text)
    json_data.update(json_data)
    i += 50
with open('../datasets/stocks/dividends_5y.json', 'w') as outf:
    json.dump(json_data, outf)
