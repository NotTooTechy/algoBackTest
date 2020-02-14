
import pandas as pd
import datetime as dt
import sys
import os
import json
import plotly
import plotly.graph_objs as go

# Import Matplotlib's `pyplot` module as `plt`
import numpy as np
from copy import deepcopy as cp
from __init__ import START_DATE, END_DATE, RISK_FACTOR, STCK_OPTIMAL_CONFIG

FONT_BUY=dict(family='Courier New, monospace', size=12, color='grey')
FONT_SELL_GREEN=dict(family='Courier New, monospace', size=16, color='green')
FONT_SELL_RED=dict(family='Courier New, monospace', size=18, color='red')


class tmethods:

	def __init__(self, ticker, cash, start=START_DATE, end=END_DATE):
		self.ticker = ticker
		self.cash = cash
		self.start = start
		self.end= end
		self.df = None
		self.mavg1 = 6
		self.mavg2 = 21
		self.annotations = []
		self.comment = None
		self.risk_factor = RISK_FACTOR
		if self.ticker in STCK_OPTIMAL_CONFIG:
			self.risk_factor = STCK_OPTIMAL_CONFIG[self.ticker]['RISK_THRESHOLD']

	def load_data_from_csv(self):
		fname = 'ALPHA_STORAGE/%s.csv'%self.ticker
		df = pd.read_csv(fname, header=0, index_col='timestamp', parse_dates=True)
		self.df = df.iloc[::-1] # reversing dataframe
		#self.df = df[(df.index > self.start) & (df.index <= self.end)]

	def set_moving_averages(self):
		min1 = "Min_%s"%self.mavg1
		avg1 = "Avg_%s"%self.mavg1
		max1 = "Max_%s"%self.mavg1

		min2 = "Min_%s"%self.mavg2
		avg2 = "Avg_%s"%self.mavg2
		max2 = "Max_%s"%self.mavg2
		# moving minimums
		self.df['min1'] = self.df['adjusted_close'].rolling(window=self.mavg1).min()
		self.df['min2'] = self.df['adjusted_close'].rolling(window=self.mavg2).min()
		# moving averages
		self.df['avg1'] = self.df['adjusted_close'].rolling(window=self.mavg1).mean()
		self.df['avg2'] = self.df['adjusted_close'].rolling(window=self.mavg2).mean()
		# min moving averages
		self.df['min_avg1'] = self.df['avg1'].rolling(window=self.mavg1).min()
		self.df['min_avg2'] = self.df['avg2'].rolling(window=self.mavg2).min()
		# max moving averages
		self.df['max_avg1'] = self.df['avg1'].rolling(window=self.mavg1).max()
		self.df['max_avg2'] = self.df['avg2'].rolling(window=self.mavg2).max()
		# moving maximums
		self.df['max1'] = self.df['adjusted_close'].rolling(window=self.mavg1).max()
		self.df['max2'] = self.df['adjusted_close'].rolling(window=self.mavg2).max()
		# differencies
		self.df['avg1-close'] = self.df['avg1'] - self.df['adjusted_close']
		self.df['avg2-close'] = self.df['avg2'] - self.df['adjusted_close']
		self.df['avg2-avg1'] = self.df['avg2'] - self.df['avg1']
		# Volatility
		self.df['Vlt'] = 10*(self.df['adjusted_close'] - self.df.shift(1, axis=0)['adjusted_close'])
		self.df['Vlt_Avg'] = self.df['Vlt'].rolling(window=self.mavg1).mean()
		# EMA
		self.df['ema'] = self.df['adjusted_close'].rolling(window=self.mavg1).mean()
		tp = 2/(self.mavg2 +1)
		self.df['ema'] = (self.df['close'] - self.df.shift(1, axis=0)['ema'])*tp + self.df.shift(1, axis=0)['ema']
		# Volume  scaled
		self.df['Volume'] = self.df['volume']/1000000.0
		# Stochastic Oscillator
		self.df['SO'] = (1.0*(self.df['adjusted_close']-self.df['min_avg1'])/(self.df['max_avg1']-self.df['min_avg1'])).rolling(window=6).mean()


	def result(self, debug=False):
		df_shifted_1 = self.df.shift(1, axis=0)
		buy_flag = False
		sell_flag = False
		sell_flag_count = 0
		buy_price = 0
		sell_price = 0
		balance = 0
		count = 0
		nprofit = 0
		nloss = 0
		threshold = 0
		risk_reference = 0
		for i, row in self.df.iterrows():
			count+=1
			risk_reference = row['adjusted_close']
			#risk_reference = row['low']
			if debug and count>2:
				#print("%10s %8s(%5.2f) %8.2f %8.2f %8s %8s"%(i.date(), row['close'], df_shifted_1[df_shifted_1.index == i]['close'], row['avg2'], row['max2'], row['buy_signal'], row['sell_signal']))
				print("%10s %8s(%5.2f, %5.2f) %8.2f %8.2f .. %8s %8s (%s)"%(i.date(), row['close'], row['low'], row['high'], row['avg1'],
					row['avg2'], buy_price, row['sell_signal'], sell_flag_count))
			if row['buy_signal'] > 0 and not buy_flag:
				buy_flag = True
				sell_flag = False
				sell_flag_count = 0
				buy_price = row['close']
				buy_date = i.date()
				#print(buy_price)
				if balance == 0:
					self.cash -= 10
					nstock = int(self.cash/row['close'])
					start_balance = buy_price*nstock
					balance = buy_price*nstock
				else:
					nstock = int(balance/buy_price)
				buy_balance = buy_price*nstock
				threshold = buy_price
				x = dict( x=i, y=row['close'], xref='x', yref='y', text='BUY', showarrow=True, arrowhead=1, ax=-40, ay=-70, font=FONT_BUY)
				self.annotations.append(x)
			elif((buy_flag and row['sell_signal']>0) or (buy_flag and risk_reference < self.risk_factor*buy_price)):
				sell_flag_count += 1
				if sell_flag_count < 6 and not (buy_flag and risk_reference < self.risk_factor*buy_price):
					continue
				sell_flag_count =0
				buy_flag = False
				sell_price = row['adjusted_close']
				if risk_reference < self.risk_factor*buy_price:
					sell_price = self.risk_factor*buy_price
				balance = sell_price*nstock - 20
				sell_date = i.date()
				if (sell_price - buy_price) >=0 :
					nprofit += 1
					x = dict( x=i, y=row['close'], xref='x', yref='y', text='SELL', showarrow=True, arrowhead=1, ax=-30, ay=-70, font=FONT_SELL_GREEN)
					print("\tDate: %10s\tBuy:%8.2f\t\tDate: %s\tSell:%8.2f\t\tGAIN:\t%8.2f\t(%8.2f, %8.2f)"%(buy_date, buy_price, sell_date, sell_price, balance - buy_balance, start_balance, balance))
				else:
					x = dict( x=i, y=row['close'], xref='x', yref='y', text='SELL', showarrow=True, arrowhead=3, ax=-30, ay=-70, font=FONT_SELL_RED)
					print("\tDate: %10s\tBuy:%8.2f\t\tDate: %s\tSell:%8.2f\t\t*LOSS:\t%8.2f\t(%8.2f, %8.2f)"%(buy_date, buy_price, sell_date, sell_price, balance - buy_balance, start_balance, balance))
					nloss += 1
				buy_price = 0
				self.comment = "(start_capital:%10.2f, balance:%10.2f)"%(start_balance, balance)
				self.annotations.append(x)
			else:
				if row['close'] > threshold:
					threshold = row['close']
		if buy_flag:
			print('Still Holding: ... ')
			current_price = row['close']
			balance = nstock*current_price
			print("\t...\tDate: %s\tBuy:%6.2f\tDate:%s\tCurrent: %6.2f\tprofit:%10.2f (%9.2f, %9.2f)"%(buy_date, buy_price, i.date(), current_price, current_price - buy_price, start_balance, balance))
		print("nprofit: {}, nloss: {}".format(nprofit, nloss))
		#print self.df.info()
		return balance



	def plotter(self):
		trace1 = go.Scatter(
			x=self.df.index, y=self.df['close'], # Data
			mode='lines', name='close'# Additional options
                )
		trace2 = go.Scatter(
			x=self.df.index, y=self.df['close'].rolling(window=self.mavg1, min_periods=1, center=False).mean(), # Data
			mode='lines', name="mean_%s"%self.mavg1, # Additional options
			visible="legendonly"
                )
		trace3 = go.Scatter(
			x=self.df.index, y=self.df['close'].rolling(window=self.mavg2, min_periods=1, center=False).mean(), # Data
			mode='lines', name="mean_%s"%self.mavg2, # Additional options
			visible="legendonly"
                )
		trace4 = go.Scatter(
			x=self.df.index, y=self.df['close'].rolling(window=self.mavg1, min_periods=1, center=False).max(), # Data
			mode='lines', name="max_%s"%self.mavg1, # Additional options
			visible="legendonly"
                )
		trace5 = go.Scatter(
			x=self.df.index, y=self.df['close'].rolling(window=self.mavg2, min_periods=1, center=False).max(), # Data
			mode='lines', name="max_%s"%self.mavg2, # Additional options
			visible="legendonly"
                )
		trace6 = go.Scatter(
			x=self.df.index, y=self.df['min_avg1'], # Data
			mode='lines', name="min_avg_%s"%self.mavg1, # Additional options
			visible="legendonly"
                )
		trace7 = go.Scatter(
			x=self.df.index, y=self.df['Vlt_Avg'], # Data
			mode='lines', name="VltAvg_%s"%self.mavg1, # Additional options
			visible="legendonly"
                )
		trace8 = go.Scatter(
			x=self.df.index, y=self.df['Volume'], # Data
			mode='lines', name="Volume/1M", # Additional options
			visible="legendonly"
                )
		trace9 = go.Scatter(
			x=self.df.index, y=self.df['SO'], # Data
			mode='lines', name="Stoh.Osc", # Additional options
			visible="legendonly"
                )
		traces = []
		traces.append(trace1)
		traces.append(trace2)
		traces.append(trace3)
		traces.append(trace4)
		traces.append(trace5)
		traces.append(trace6)
		traces.append(trace7)
		traces.append(trace9)

		layout = go.Layout(title="%s, %s"%(self.ticker.upper(),self.comment), plot_bgcolor='rgb(230, 230,230)', annotations=self.annotations)
		fig = go.Figure(data=traces, layout=layout)
		plot_filename = "%s.html"%self.ticker
		plotly.offline.plot(fig, filename=plot_filename)
