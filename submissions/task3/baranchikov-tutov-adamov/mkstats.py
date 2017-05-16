#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np

import sys
from os import listdir, makedirs
from os.path import isfile, join, exists

def process_store(sell, supply, inventory, sell_parser):
    supply.set_index('date', inplace=True)
    inventory.set_index('date', inplace=True)
    sell.sku_num = sell.sku_num.map(sell_parser)
    
    def apple(daily): 
        return np.sum(daily == 'a')
    def pen(daily): 
        return np.sum(daily == 'p')
    
    sells_daily = sell.groupby('date')['sku_num'].agg([apple, pen])
    changes_daily = supply.reindex_like(sells_daily).fillna(0) - sells_daily
    
    monthly_cumsum_changes = \
        changes_daily.groupby(lambda date: date[:-2]).agg(np.cumsum)
    # небольшой хак: расширяем фрейм на каждый день, 
    # заполняя поле состоянием склада в последний день предыдущего месяца, 
    # в начале склад пуст
    extend_inventory = inventory.reindex_like(monthly_cumsum_changes).\
        shift(1).fillna(axis=0, method='ffill').fillna(0)
    
    store_daily_state = extend_inventory + monthly_cumsum_changes
    stolen_monthly = store_daily_state.reindex_like(inventory) - inventory
    
    return store_daily_state, stolen_monthly, \
        sells_daily.groupby(lambda date: date[:-2]).sum()

def agregate_statistics(stats):
    return pd.concat(stats).groupby(['year', 'state']).sum()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise Exception('Not enough arguments')

    sell_parser = lambda transaction: transaction[6]

    inp_dir = sys.argv[1]
    out_dir = sys.argv[2]

    all_files = [f for f in listdir(inp_dir) if isfile(join(inp_dir, f))]
    stores = [f[:-8] for f in all_files if f[-8:] == "sell.csv"]

    if not exists(out_dir):
        makedirs(out_dir)
        
    statistics = []
    for store in stores:
        print "Processing \"{0}\"".format(store[:-min(len(store), 1)])
        try:
            inventory = pd.read_csv(inp_dir + '/' + store + 'inventory.csv')
            sold = pd.read_csv(inp_dir + '/' + store + 'sell.csv')
            supply = pd.read_csv(inp_dir + '/' + store + 'supply.csv')
        except:
            print "Error while reading \"{0}\" files, ignore". \
                format(store[:-min(len(store), 1)])
            continue
        
        state, stolen, sells = process_store(sold, supply, inventory, sell_parser)
        
        state.to_csv(out_dir + '/' + store + 'daily.csv')
        stolen.to_csv(out_dir + '/' + store + 'steal.csv')
        
        sells.index = stolen.index
        stats = sells.join(stolen, lsuffix='_sold', rsuffix='_stolen').reset_index()
        stats['state'] = store[:2]
        stats['year'] = stats.date.map(lambda date: date[:4])
        del stats['date']
        statistics.append(stats)

    agregate_statistics(statistics).to_csv(out_dir + '/states.csv')
