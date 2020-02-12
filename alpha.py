import sys
import os
import json
import csv
import requests
from __init__ import api_key

INTRADAY_MINS=5
intraday_link="https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=%s&interval=%smin&apikey=%s"
DATA_DIR="ALPHA_STORAGE"

symbol=sys.argv[1]
#print(intraday_link%(symbol, INTRADAY_MINS, api_key))
#r = requests.get(intraday_link%(symbol, INTRADAY_MINS, api_key))
#print r
#print r.json()

class alphavantage:
	def __init__(self, symbol):
		self.symbol = symbol

	def get_full_history(self, rtype='json'):
		if rtype == 'json':
			LINK = '''https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=%s&outputsize=full&apikey=%s'''%(self.symbol, api_key)
			r = requests.get(LINK)
			if r.status_code == 200:
				data = r.json()
				fpath = os.path.join(DATA_DIR, "%s.json"%self.symbol)
				print(fpath)
				with open(fpath, 'w') as f:
					json.dump(data, f, indent=4)
		elif rtype == 'csv':
			LINK = '''https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=%s&outputsize=full&apikey=%s&datatype=csv'''%(self.symbol, api_key)
			r = requests.get(LINK)
			if r.status_code == 200:
				data = r.content
				fpath = os.path.join(DATA_DIR, "%s.csv"%self.symbol)
				print(fpath)
				with open(fpath, 'w') as f:
					f.write(data)



if __name__ == "__main__":
	stock = sys.argv[1]
	alpha = alphavantage(stock)
	alpha.get_full_history('csv')
