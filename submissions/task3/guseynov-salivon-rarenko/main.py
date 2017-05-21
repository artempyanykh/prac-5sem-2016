import sys
import numpy as np
import pandas as pd
from os import listdir, makedirs
from os.path import exists, isfile, join

import datetime
from collections import OrderedDict


def get_daily(supply, sell, inventory):
    def apple(value):
        return np.sum(value == 'ap')

    def pen(value):
        return np.sum(value == 'pe')

    sell['good'] = sell.sku_num.apply(lambda transaction: transaction.split('-')[2])
    sold_by_day = sell.groupby('date').good.agg([apple, pen])

    supply = supply.set_index('date').reindex_like(sold_by_day).fillna(0)
    daily_state = (supply - sold_by_day).groupby(lambda date: date[:-2]).agg(np.cumsum)
    inventory = inventory.set_index('date')
    for inv in inventory.itertuples():
        next_day = np.datetime64(inv[0]) + 1
        month = str(next_day)[:-2]
        daily_state['apple'][month:month+'31'] += inv[1]
        daily_state['pen'][month:month+'31'] += inv[2]
    stolen = daily_state.reindex_like(inventory) - inventory
    return daily_state, stolen, sold_by_day

if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise Exception('Not enough arguments')

    inp_dir = sys.argv[1]
    out_dir = sys.argv[2]

    all_files = [f for f in listdir(inp_dir) if isfile(join(inp_dir, f))]
    stores = [f[:-8] for f in all_files if f[-8:] == "sell.csv"]

    if not exists(out_dir):
        makedirs(out_dir)
    all_stats = []

    for store in stores:
        print "Processing \"{0}\"".format(store[:-min(len(store), 1)])
        try:
            inventory = pd.read_csv(inp_dir + '/' + store + 'inventory.csv')
            sell = pd.read_csv(inp_dir + '/' + store + 'sell.csv')
            supply = pd.read_csv(inp_dir + '/' + store + 'supply.csv')
        except:
            print "Error while reading \"{0}\" files, ignore". \
                format(store[:-min(len(store), 1)])
            continue

        daily, steal, sold = get_daily(supply, sell, inventory)
        daily.to_csv(out_dir + '/' + store + 'daily.csv')
        steal.to_csv(out_dir + '/' + store + 'steal.csv')
        steal = steal.reindex_like(daily).fillna(0)
        steal = steal.reset_index()
        sold = sold.reset_index()
        state_stats = OrderedDict()
        state_stats['year'] = sold['date'].apply(lambda date: date[:4])
        state_stats['state'] = store[:2]
        state_stats['apple_sold'] = sold['apple']
        state_stats['apple_stolen'] = steal['apple']
        state_stats['pen_sold'] = sold['pen']
        state_stats['pen_stolen'] = steal['pen']
        all_stats.append(pd.DataFrame(state_stats))

    states = pd.concat(all_stats).groupby(['year', 'state']).sum()
    states.to_csv(out_dir + '/states.csv')
    