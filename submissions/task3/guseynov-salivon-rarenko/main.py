import os
import sys
import collections
import pandas as pd

from collections import defaultdict


class Solution:
    state_data_headers = ['year', 'state', 'apple_sold', 'apple_stolen', 'pen_sold', 'pen_stolen']
    stolen_data_headers = ['date', 'apple', 'pen']
    daily_inv_data_headers = ['date', 'apple', 'pen']

    def __init__(self):
        self.state_data = []
        self.stolen_data = []
        self.daily_inv_data = []

        self.inv_data = defaultdict(dict)
        self.sold_data = defaultdict(dict)
        self.supply_data = defaultdict(dict)

    def load_data(self, inv_file, sold_file, supply_file):
        try:
            self.inv = pd.read_csv(inv_file)
            self.sold = pd.read_csv(sold_file)
            self.supply = pd.read_csv(supply_file)
        except:
            exit('Couldn\'t load data')

        self.state = ''
        self.sold_data = defaultdict(dict)
        self.inv_data = defaultdict(dict)
        self.supply_data = defaultdict(dict)
        self.stolen_data = []
        self.daily_inv_data = []

    def process_data(self):
        for _, date, sku_num in self.sold.itertuples():
            sku_num = sku_num.split('-')
            self.state, item = sku_num[0], sku_num[2]
            if not self.sold_data[date]:
                self.sold_data[date]['ap'] = 0
                self.sold_data[date]['pe'] = 0
            self.sold_data[date][item] += 1
        for _, date, apple, pen in self.inv.itertuples():
            self.inv_data[date]['ap'] = apple
            self.inv_data[date]['pe'] = pen
        for _, date, apple, pen in self.supply.itertuples():
            self.supply_data[date]['ap'] = apple
            self.supply_data[date]['pe'] = pen

    def count_all(self):
        start_date, finish_date = self.supply['date'][0], self.inv['date'][len(self.inv) - 1]
        all_dates = pd.date_range(start_date, finish_date, freq='D')

        state_index = len(self.state_data)
        for index, val in enumerate(self.state_data):
            if self.state == val[1]:
                state_index = index
                break
        state_index -= 1

        cur_apples = 0
        cur_pen = 0
        for cur_date in all_dates:
            if cur_date.day == cur_date.month == 1:
                state_index += 1
                if state_index == len(self.state_data):
                    self.state_data.append([cur_date.year, self.state, 0, 0, 0, 0])

            date = str(cur_date).split()[0]
            supply_data, sold_data, inv_data = self.supply_data[date], self.sold_data[date], self.inv_data[date]
            if supply_data:
                cur_apples += supply_data['ap']
                cur_pen += supply_data['pe']
            if sold_data:
                apples_sold, pen_sold = sold_data['ap'], sold_data['pe']
                cur_apples -= apples_sold
                cur_pen -= pen_sold
                self.state_data[state_index][2] += apples_sold
                self.state_data[state_index][4] += pen_sold
            if inv_data:
                apples_stolen, pen_stolen = cur_apples - inv_data['ap'], cur_pen - inv_data['pe']
                self.stolen_data.append([date, apples_stolen, pen_stolen])
                self.state_data[state_index][3] += apples_stolen
                self.state_data[state_index][5] += pen_stolen
                cur_apples = self.inv_data[date]['ap']
                cur_pen = self.inv_data[date]['pe']
            self.daily_inv_data.append([date, cur_apples, cur_pen])

    def get_shop_data(self):
        return (pd.DataFrame(self.daily_inv_data, columns=self.daily_inv_data_headers),
                pd.DataFrame(self.stolen_data, columns=self.stolen_data_headers))

    def get_states_data(self):
        return pd.DataFrame(self.state_data, columns=self.state_data_headers)


def solve():
    input_directory, outut_directory = sys.argv[1], sys.argv[2]
    sell_data = [file[:-9] for file in os.listdir(input_directory) if "sell.csv" in file]

    if not os.path.exists(outut_directory):
        os.makedirs(outut_directory)

    solution = Solution()
    for sell_file in sell_data:
        print "Processing %s" % sell_file

        solution.load_data(input_directory + '/' + sell_file + '-' + 'inventory.csv',
                           input_directory + '/' + sell_file + '-' + 'sell.csv',
                           input_directory + '/' + sell_file + '-' + 'supply.csv')
        print('Data loaded')
        solution.process_data()
        solution.count_all()

        shop_daily, shop_steal = solution.get_shop_data()
        shop_daily.to_csv(outut_directory + '/' + sell_file + '-' + 'daily.csv', index=False)
        shop_steal.to_csv(outut_directory + '/' + sell_file + '-' + 'steal.csv', index=False)

    solution.get_states_data().to_csv(outut_directory + '/states.csv', index=False)


if __name__ == "__main__":
    solve()
