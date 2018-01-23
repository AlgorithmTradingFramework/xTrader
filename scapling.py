import data_handling, sample
import numpy as np
def ready_data():
	data = sample.load_history()
	data = sample.ready_data(data)
	rdata = []
	for i in data:
		rdata += i[1:-1]
	return rdata

def scaple(prices):
	state, buy, cap = 1, 0, 0
	profits = []
	for i, price in enumerate(prices):
		if state and np.random.randint(2):
			state, buy = 0, price
			# print('bought at step: {}, price: {}'.format(i, price))
			# state, buy = (0, price) if np.random.randint(2) else (1, 0)
			continue
		if not state:
			diff = price*(.99) - buy*(1.005)
			if abs(diff)/buy > 0.1:
				# print('sold at step: {}, price: {}, diff: {}'.format(i, price, diff))
				state = 1
				cap += diff
				profits.append(diff)
	return (np.asarray(profits), cap)


def martingale(prices):
	state, buy, cap = 1, 0, 0
	profits, vol = [], 1
	for i, price in enumerate(prices):
		if state and np.random.randint(2):
			state, buy = 0, price
			# print('bought at step: {}, price: {}'.format(i, price))
			# state, buy = (0, price) if np.random.randint(2) else (1, 0)
			continue
		if not state:
			diff = price*(.99) - buy*(1.005)
			if abs(diff)/buy > 0.1:
				if diff > 0:
					# print('sold at step: {}, price: {}, diff: {}'.format(i, price, diff))
					state = 1
					cap += vol * diff
					print(vol)
					vol = 1
					profits.append(diff)
				else:
					vol *= 2
					buy = price
	return (np.asarray(profits), cap)



# scaple(ready_data())
# import scapling as s
# rep = {'c':[], 'l': [], 'w':[]}

# for i in range(1,20):
# 	result, c = scaple(ready_data())
# 	l , w = len(result), np.cumsum(result>0)[-1] 
# 	# rep['c'].append(c); rep['l'].append(l); rep['w'].append(w)
# 	print(l, w, c)
# 	# print('summery:')
# 	# print('tardes: {}, wins: {}, capital: {}'.format(sum(rep['l'])/i, (sum(rep['w'])/i), (sum(rep['c'])/i) ))


martingale(ready_data())

for i in range(1,20):
	result, c = martingale(ready_data())
	l , w = len(result), np.cumsum(result>0)[-1] 
	# rep['c'].append(c); rep['l'].append(l); rep['w'].append(w)
	print(l, w, c)
