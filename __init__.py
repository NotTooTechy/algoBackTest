import sys
import datetime

#START_DATE=datetime.datetime(2016, 1, 16)
#START_DATE=datetime.datetime(2016, 9, 16)
START_DATE=datetime.datetime(2018, 2, 4)
#START_DATE=datetime.datetime(2017, 8, 10)
#START_DATE=datetime.datetime(2019, 2, 10)
#START_DATE=datetime.datetime(2016, 6, 17)
#START_DATE=datetime.datetime(2019, 1, 17)
#START_DATE=datetime.datetime(2009, 1, 1)
#START_DATE=datetime.datetime(2017, 1, 1)
#START_DATE=datetime.datetime(2007, 9, 16)
END_DATE=datetime.datetime.now()
#END_DATE=datetime.datetime(2019, 10, 17)
#END_DATE=datetime.datetime(2019, 02, 04) #2018-05-16

#alpha: https://www.alphavantage.co/support/#api-key
api_key="EAE489DPENMJ722N"


#START_DATE=datetime.datetime(2015, 1, 19)
#START_DATE=datetime.datetime(2018, 7, 6)

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

def chk_arg(argument):
        if any(argument in s for s in sys.argv):
                        index = [i for i, s in enumerate(sys.argv) if argument in s][0]
                        try:
                            ret = sys.argv[index].split('=')[1]
                        except:
                            return None
                        return ret
        return None
