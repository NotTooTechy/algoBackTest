import sys
from __init__ import TEST_DATES_LIST
from stockbase import tmethods

def get_line_arg(line_arg):
	if any(line_arg in x for x in sys.argv[1:]):
		for x in sys.argv[1:]:
			if line_arg in x:
				value = x.split("=")[1]
				return value
	return None

def check_arg(line_arg):
	if line_arg in sys.argv:
		return True
	return False

class strategies(tmethods):
	''' Define Strategies '''

	def strategy2(self):
		#df_shifted_1 = self.df.shift(1, axis=0)
		print(">"*20, self.start.date(), self.end.date(), "<"*20)
		self.df['buy_signal'] = 0
		self.df['sell_signal'] = 0
		self.result()
		self.df['sell_signal'] = self.df[
			(self.df['close'] < self.df['avg1'])
			]['close']
		self.df['risk_signal'] = self.df[
			(self.df['close'] < 0.9*self.df.shift(1, axis=0)['close'])
			]['close']
		self.df['buy_signal'] = self.df[
			(self.df['close'] > self.df['avg1'])&
			(self.df['close'] > self.df['avg2'])
			]['close']

	def strategy3(self):
		print(">"*20, self.start.date(), self.end.date(), "<"*20)
		self.df['buy_signal'] = 0
		self.df['sell_signal'] = 0
		self.df['sell_signal'] = self.df[
			(self.df['close'] < self.df['avg2'])
			]['close']

		self.df['buy_signal'] = self.df[
			#(self.df['close'] > self.df['avg1'])&
			(self.df['close'] > self.df['avg2'])&
			(self.df['avg1'] > self.df['avg2'])&
			(self.df['avg1'] > self.df.shift(1, axis=0)['avg1'])&
			(self.df['avg2'] > self.df.shift(1, axis=0)['avg2'])&
			(self.df.shift(1, axis=0)['avg2'] > self.df.shift(2, axis=0)['avg2'])
			]['close']
		#self.df.to_csv("extended_%s.csv"%self.ticker, sep='\t')
		print(self.df.tail())

	def strategy4(self):
		print(">"*20, self.start.date(), self.end.date(), "<"*20)
		self.df['buy_signal'] = 0
		self.df['sell_signal'] = 0
		self.df['sell_signal'] = self.df[
			(self.df['close'] > self.df['ema'])&
			(self.df['close'] < self.df['avg1'])#|
			#(self.df['close'] >= self.df['max_avg2'])
			#(self.df['SO'] < 0)
			]['close']

		self.df['buy_signal'] = self.df[
			(self.df['close'] > self.df['ema'])&
			(self.df['close'] > self.df['avg1'])
			#(self.df['SO'] >= 0)
			]['close']

	def strategy5(self):
		print(">"*20, self.start.date(), self.end.date(), "<"*20)
		self.df['buy_signal'] = 0
		self.df['sell_signal'] = 0

		self.df['sell_signal'] = self.df[
			(self.df['close'] < self.df['avg1'])
			]['close']

		self.df['buy_signal'] = self.df[
			(self.df['close'] > self.df['avg1'])&
			(self.df['close'] > 1.01*self.df.shift(1, axis=0)['close'])
			]['close']

class runroutine(strategies):

	def run_routine(self, debug=False, graph=False, avg1=6, avg2=50):
		self.load_data_from_csv()
		self.df = self.df[(self.df.index > self.start) & (self.df.index <= self.end)]
		self.mavg1=avg1
		self.mavg2=avg2
		self.set_moving_averages()
		print(self.mavg1, self.mavg2)
		self.strategy2()
		self.result(debug)
		if graph:
			self.plotter()

	def run_routine2(self, debug=False, graph=False, avg1=6, avg2=50):
		self.load_data_from_csv()
		self.df = self.df[(self.df.index > self.start) & (self.df.index <= self.end)]
		#print(avg1, avg2)
		self.mavg1=avg1
		self.mavg2=avg2
		self.set_moving_averages()
		self.strategy4()
		self.result(debug)
		print
		if graph:
			self.plotter()

	def run_sanity(self, debug=False, strategy_name='strategy5'):
		self.load_data_from_csv()
		results = []
		for start_date in TEST_DATES_LIST:
			self.start = start_date
			self.df = self.df[(self.df.index > self.start) & (self.df.index <= self.end)]
			max_balance = 0
			best_avg = 0
			for avg1 in range(2, 50):
				self.mavg1=avg1
				self.set_moving_averages()
				self.strategy5()
				#getattr(self, strategy_name)()
				balance = self.result(debug)
				if balance > max_balance:
					max_balance = balance
					best_avg = avg1
			_res_dict = {
				'date': start_date.strftime("%m/%d/%Y"),
				'avg': best_avg,
				'balance': max_balance
				}
			results.append(_res_dict)
		print("The best cases for {}:".format(self.ticker))
		for res in results:
			print(res)

	def run_routine5(self, debug=False, graph=False, avg1=6, avg2=50):
		self.load_data_from_csv()
		self.df = self.df[(self.df.index > self.start) & (self.df.index <= self.end)]
		print(avg1, avg2)
		self.mavg1=avg1
		self.mavg2=avg2
		self.set_moving_averages()
		self.strategy5()
		print(self.result(debug))
		print
		if graph:
			self.plotter()

if __name__=='__main__':
	import sys
	debug = False
	graph = False
	cash = 17000
	avg1 = 6
	if check_arg('debug'):
		debug = True
	if check_arg('graph'):
		graph = True
	if get_line_arg('cash') is not None:
		cash = float(get_line_arg('cash'))
	if get_line_arg('avg1') is not None:
		avg1 = int(get_line_arg('avg1'))
	if get_line_arg('avg2') is not None:
		avg2 = int(get_line_arg('avg2'))
	else:
		avg2 = avg1
	if get_line_arg('ticker') is not None:
		ticker = get_line_arg('ticker')
	stck = runroutine(ticker, cash)
	if 'sanity' in sys.argv:
		stck.run_sanity()
	else:
		stck.run_routine5(debug, graph, avg1, avg2)
