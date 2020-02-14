import sys
import datetime

START_DATE=datetime.datetime(2018, 2, 4)
#START_DATE=datetime.datetime(2017, 8, 10)

END_DATE=datetime.datetime.now()
#END_DATE=datetime.datetime(2019, 10, 17)

#alpha: https://www.alphavantage.co/support/#api-key
api_key="EAE489DPE5MJ721N" # obsolete you need to get your own


RISK_FACTOR = 0.9

STCK_OPTIMAL_CONFIG = {
	'uwt': {'RISK_THRESHOLD': 0.85, 'mavg1': 6, 'strategy': 'strategy5'},
	'hou.to': {'RISK_THRESHOLD': 0.9, 'mavg1': 6, 'strategy': 'strategy5'},
	'bbd-b.to': {'RISK_THRESHOLD': 0.9, 'mavg1': 10, 'strategy': 'strategy5'}
}

TEST_DATES_LIST = [
	datetime.datetime(2017, 2, 5),
	datetime.datetime(2017, 8, 5),
	datetime.datetime(2018, 2, 5),
	datetime.datetime(2018, 8, 5),
	datetime.datetime(2019, 2, 5)
]
