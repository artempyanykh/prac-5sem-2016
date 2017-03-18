import sys
import collections
import pandas as pd

from os import listdir, makedirs
from os.path import isfile, join, exists

nested_dict = lambda: collections.defaultdict(nested_dict)


class Solution:
    def __init__(self):
        self.inv    = None
        self.sold   = None
        self.supply = None
        self.start_date = None
        self.finish_date = None
        self.state = ''

        self.state_stats_headers     = ['year', 'state', 'apple_sold', 'apple_stolen', 'pen_sold', 'pen_stolen']
        self.stolen_stats_headers    = ['date', 'apples', 'pens']
        self.daily_inv_stats_headers = ['date', 'apples', 'pens']

        self.state_stats     = []
        self.stolen_stats    = []
        self.daily_inv_stats = []

        self.sold_stats   = nested_dict()
        self.inv_stats    = nested_dict()
        self.supply_stats = nested_dict()

    def shop_add(self, inv, sold, supply):
        self.inv = inv
        self.sold = sold
        self.supply = supply
        self.start_date  = self.supply['date'][0]
        self.finish_date = self.inv['date'][len(inv) - 1]
        self.state = ''
        self.sold_stats   = nested_dict()
        self.inv_stats    = nested_dict()
        self.supply_stats = nested_dict()
        self.stolen_stats     = []
        self.daily_inv_stats = []

    def shop_build_stats(self):
        def parse_sku_num(sku_num):
            tmp = sku_num.split('-')
            return tmp[0], tmp[2]
        for idx, row in self.sold.iterrows():
            self.state, type = parse_sku_num(row['sku_num'])
            if not self.sold_stats[row['date']]:
                self.sold_stats[row['date']]['ap'] = 0
                self.sold_stats[row['date']]['pe'] = 0
            self.sold_stats[row['date']][type] += 1
        for idx, row in self.inv.iterrows():
            self.inv_stats[row['date']]['ap'] = row['apple']
            self.inv_stats[row['date']]['pe'] = row['pen']
        for idx, row in self.supply.iterrows():
            self.supply_stats[row['date']]['ap'] = row['apple']
            self.supply_stats[row['date']]['pe'] = row['pen']

    def calc_answer(self):
        pd_dates = pd.date_range(self.start_date, self.finish_date, freq='D')

        state_stats_idx = len(self.state_stats)
        for idx, val in enumerate(self.state_stats):
            if self.state == val[1]:
                state_stats_idx = idx
                break
        state_stats_idx -= 1

        cur_apples = 0
        cur_pens   = 0
        for pd_date in pd_dates:
            if pd_date.day == 01 and pd_date.month == 01:
                state_stats_idx += 1
                if state_stats_idx == len(self.state_stats):
                    self.state_stats.append([pd_date.year, self.state, 0, 0, 0, 0])

            date = str(pd_date).split()[0]
            if self.supply_stats[date]:
                cur_apples += self.supply_stats[date]['ap']
                cur_pens   += self.supply_stats[date]['pe']
            if self.sold_stats[date]:
                cur_apples -= self.sold_stats[date]['ap']
                cur_pens   -= self.sold_stats[date]['pe']
                self.state_stats[state_stats_idx][2] += self.sold_stats[date]['ap']
                self.state_stats[state_stats_idx][4] += self.sold_stats[date]['pe']
            if self.inv_stats[date]:
                apples_stolen, pens_stolen = (cur_apples - self.inv_stats[date]['ap'], cur_pens - self.inv_stats[date]['pe'])
                self.stolen_stats.append([date, apples_stolen, pens_stolen])
                self.state_stats[state_stats_idx][3] += apples_stolen
                self.state_stats[state_stats_idx][5] += pens_stolen
                cur_apples = self.inv_stats[date]['ap']
                cur_pens   = self.inv_stats[date]['pe']
            self.daily_inv_stats.append([date, cur_apples, cur_pens])

    def shop_get_answer(self):
        return (pd.DataFrame(self.daily_inv_stats, columns=self.daily_inv_stats_headers),
                pd.DataFrame(self.stolen_stats, columns=self.stolen_stats_headers))

    def states_get_answer(self):
        return pd.DataFrame(self.state_stats, columns=self.state_stats_headers)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise Exception('Not enough arguments')

    inp_dir = sys.argv[1]
    out_dir = sys.argv[2]

    all_files = [f for f in listdir(inp_dir) if isfile(join(inp_dir, f))]
    data_sets = [f[:-8] for f in all_files if f[-8:] == "sell.csv"]

    if not exists(out_dir):
        makedirs(out_dir)

    sol = Solution()
    for ds in data_sets:
        print "Processing \"{0}\" dataset...".format(ds[:-min(len(ds), 1)])
        try:
            inv    = pd.read_csv(inp_dir + '/' + ds + 'inventory.csv')
            sold   = pd.read_csv(inp_dir + '/' + ds + 'sell.csv')
            supply = pd.read_csv(inp_dir + '/' + ds + 'supply.csv')
        except:
            print "Error while reading \"{0}\" files, ignore".format(ds[:-min(len(ds), 1)])
            continue

        sol.shop_add(inv, sold, supply)
        sol.shop_build_stats()
        sol.calc_answer()

        shop_daily, shop_steal = sol.shop_get_answer()
        shop_daily.to_csv(out_dir + '/' + ds + 'daily.csv', index=False)
        shop_steal.to_csv(out_dir + '/' + ds + 'steal.csv', index=False)

    sol.states_get_answer().to_csv(out_dir + '/states.csv', index=False)