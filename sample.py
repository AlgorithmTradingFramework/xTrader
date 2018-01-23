import pandas as pd
from os import listdir, getcwd
import json, data_handling, inspect
import pandas as pd
import numpy as np
import backtest as bt


'''
you will need to overwrite this modual,
it is simple sample of how to use this library. 
'''


def load_history(symbol_id='Stock1'):
    '''
    this function gets string symboli_id which is your symbol name and returns its histroy,
    overwrite it to connect to your data base but don't change the out put structure,
    it should be a dictionary and each value is a list of values in ascendting way corresponding to time 
    '''
	with open('result.json', 'r') as f:
		data = json.load(f)[symbol_id]
		f.close()
	return data


def create_data(*args, **kwargs):
    '''
    this function create a redult.json file that performs as database,
    once you set a database and you don't need this fuction any more then overwrite load_history function. 
    '''
    names = {'date':'<DTYYYYMMDD>','high': '<HIGH>', 'low': '<LOW>', 'close': '<CLOSE>', 'volume': '<VOL>', 'open':'<OPEN>'}
    def read_file_names(sufix=['csv'], directory=getcwd()):
        return {file:'.'.join(file.split('.')[:-1]) for file in listdir(directory) if file.split('.')[-1] in sufix}

    data = dict()
    files = read_file_names(*args, **kwargs)
    for file, symbol_id in files.items():
    	df = pd.read_csv(file)
    	data[symbol_id] = {name: [value for value in df[nickname]][::-1] for name, nickname in names.items()}

    with open('result.json', 'w') as fp:
        json.dump(data, fp)
        fp.close()



data = {
	'kind': 'ascending',
	'indicators':{
		'ascending': {
			'apply_to': 'close',
			'name': 'sma',
			'outputs': ['real'],
			'output': {
				'name':'real',
			},
			'params': {
				'timeperiod': 5,
			},
			'settings': {
				'shift': 0,
			}
		},
	},
	'days': 3,
	'valid': 2,
	'symbol_id': 'Saipa',

}


def backtest(results):
    symbol_id = 'Saipa'
    first_kind_dict, second_kind_dict, final_dict = {}, {}, {}
    first, second, bad_symbol = False, False, False
    for index, result in enumerate(results):
        if result['type'] == 'first':
            first_kind_dict['filter-first {}'.format(index)] = make_list_ready(result['result'])
            first = True
        if result['type'] == 'second':
            second_kind_dict['filter-second {}'.format(index)] = make_list_ready(result['result'])
            second = True
    if first:
        final_dict['first'] = check_first_kind(first_kind_dict)
    if second:
        final_dict['second'] = check_second_type(second_kind_dict)
    final = final_check(final_dict)
    backtest = data_handling.give_result_backtest(name=symbol_id, res=final,
                                       config={
                                       	'take profit': {'apply': 'close', 'value': 0 },
                                       	'stop loss': {'apply': 'close', 'value': 0},
										'initial deposit': '1000000',
										})
    return backtest

def check_first_kind(results):
    magic_number = len(results)
    first = pd.DataFrame(results)
    result = first.sum(axis=1)
    check = result.apply(lambda x: 0 if (x < magic_number and x > -magic_number) else x)
    check = check.replace([magic_number, -magic_number], [1, -1])
    return np.asarray(check)


def check_second_type(results):
    second = pd.DataFrame(results)
    result = second.product(axis=1)
    return np.asarray(result)


def final_check(final_dict):
    df = pd.DataFrame(data=final_dict)
    return np.asarray(df.product(axis=1))


def make_list_ready(unready_list):
    return [x[0] for x in eval(unready_list)]

def report_backtest(results):
    dohlcv = load_history()
    dohlcv = ready_data(dohlcv)
    # dohlcv = [[0]*6 for i in range(5000)]
    res = results['result'];
    num_of_trades = len(res.keys())
    buy_b, sell_b, tbl = [], [], []
    if (num_of_trades != 0):
        row_num = 0
        for i in range(num_of_trades, 0, -1):
            if (len(res[str(i)].keys()) == 2):
                tbl = [num_of_trades - i + 1, dohlcv[int(res[str(i)]["sell"]["date"])][0], res[str(i)]["sell"]['action'], dohlcv[int(res[str(i)]["sell"]["date"])][4], 'NaN', res[str(i)]["sell"]["candles in trade"], res[str(i)]["sell"]["return"], res[str(i)]["sell"]["capital"]];
                # if (res[str(i)]["sell"]['action'] != 'Not Sold Yet') {
                #     sell_b.unshift([dohlcv[res[str(i)]["sell"]["date"]][0], dohlcv[res[str(i)]["sell"]["date"]][2]]);
                # }
                appendRow(tbl, row_num);
                row_num += 1;
            else:
                # // console.log('no sold yet');
                tbl = [num_of_trades - i + 1, dohlcv[dohlcv.length - 1][0], res[str(i)]["sell"]['action'], 'NaN', 'NaN', 'NaN', "NaN", "NaN"];
                appendRow(tbl, row_num);
                row_num += 1;
            
            if (i == 1):
                tbl = [num_of_trades - i + 1, dohlcv[int(res[str(i)]["buy"]["date"])][0], res[str(i)]["buy"]['action'],  dohlcv[int(res[str(i)]["buy"]["date"])][4], res[str(i)]["buy"]["waiting candles"], 'NaN', 'NaN', 'Initial Deposit: ' + str(numberSeparator(res[str(i)]["buy"]["initaial deposit"]))];
                # buy_b.unshift([dohlcv[res[str(i)]["buy"]["date"]][0], dohlcv[res[str(i)]["buy"]["date"]][2]]);
                appendRow(tbl, row_num);
                row_num += 1;
            else:
                tbl = [num_of_trades - i + 1, dohlcv[int(res[str(i)]["buy"]["date"])][0], res[str(i)]["buy"]['action'], dohlcv[int(res[str(i)]["buy"]["date"])][4], res[str(i)]["buy"]["waiting candles"], 'NaN', 'NaN', 'NaN'];
                # buy_b.unshift([dohlcv[res[str(i)]["buy"]["date"]][0], dohlcv[res[str(i)]["buy"]["date"]][2]]);
                appendRow(tbl, row_num);
                row_num += 1;
           
        avg = results['summery']['average']
        tbl = ['', '', '', 'Average', avg['waiting candles'], avg['candles in trade'], avg['profits'], "NaN"];
        appendRow(tbl, row_num)
        row_num += 1;

        std = results['summery']['std'];
        tbl = ['', '', '', 'Standard Deviation', std['waiting candles'], std['candles in trade'], str(std['profits']) + '%', "NaN"];
        appendRow(tbl, row_num);
        row_num += 1;
    else:
        print('No trade find with this strategy!')


def appendRow(rep, num):
	print(num, ' '.join(str(i) for i in rep))

def numberSeparator(i):
	return i

# calc_one_filter(data)
'''
import configs as c
data = c.data
a = c.calc_one_filter(data)
b = c.backtest([eval(a)])
c.report_backtest(eval(b))
'''
# import configs as c
# a = c.t()

def ready_data(data):
	n = len(data['date'])
	dohlcv = []
	for i in range(0, n):
		day = []
		for title in  ['date', 'open', 'high', 'low', 'close', 'volume']:
			day.append(data[title][i])
		dohlcv.append(day)
	return dohlcv
