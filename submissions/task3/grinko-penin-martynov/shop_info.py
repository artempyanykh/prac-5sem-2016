import pandas as pnd
import numpy as np
import datetime

def update_bank(x) :
    if x.day == 1 or x.day == 15:
        return True
    else:
        return False

print("Please, use keyboard to input your shop's data file names")
print("Please, enter the supply file name:")
supply_path = input()
print("Please, enter the sell file name:")
sell_path = input()
print("Please, enter the inventory file name:")
inventory_path = input()
        
supply = pnd.read_csv(supply_path, parse_dates = ["date"], dtype = {"apple":np.int64, "pen":np.int64})
sell = pnd.read_csv(sell_path, parse_dates = ["date"])
inventory = pnd.read_csv(inventory_path, parse_dates = ["date"], dtype = {"apple":np.int64, "pen":np.int64})

columns = ["date", "apple", "pen"]

daily = pnd.DataFrame(columns = columns)
stolen = pnd.DataFrame(columns = columns)

stolen["date"] = inventory["date"]

apple_list = []

pen_list = []

apple_box = 0

pen_box = 0

index = 0
index_2 = 0

apple_stolen = []

pen_stolen = []

mask_a = sell.sku_num.str[6:8] == "ap"
mask_b = sell.sku_num.str[6:8] == "pe"

apple_part = sell.loc[mask_a]
pen_part = sell.loc[mask_b]

apple_database = apple_part.groupby(["date"])["sku_num"]
pen_database = pen_part.groupby(["date"])["sku_num"]

apple_count = apple_database.count()
pen_count = pen_database.count()

for dates in apple_count.index :
    if update_bank(dates) == True :
        apple_box += supply["apple"][index]
        pen_box += supply["pen"][index]
        index += 1
    apple_box -= apple_count[dates]
    pen_box -= pen_count[dates]
    if (dates + datetime.timedelta(days = 1)).month != dates.month :
        apple_stolen.append(apple_box - inventory["apple"][index_2])
        pen_stolen.append(pen_box - inventory["pen"][index_2])
        apple_box = inventory["apple"][index_2]
        pen_box = inventory["pen"][index_2]
        index_2 += 1
    apple_list.append(apple_box)
    pen_list.append(pen_box)
    
daily["date"] = apple_count.index
daily["apple"] = apple_list
daily["pen"] = pen_list
stolen["apple"] = apple_stolen
stolen["pen"] = pen_stolen

daily.to_csv(supply_path[:6] + "daily.csv", index = False)
stolen.to_csv(supply_path[:6] + "steal.csv", index = False)

t_columns = ["year", "state", "apple_sold", "pen_sold", "apple_stolen", "pen_stolen"]
temporary = pnd.DataFrame(columns = t_columns)

key = lambda x: x.year

apple_sold = apple_count.groupby(key).sum()
pen_sold = pen_count.groupby(key).sum()
stolen_summary = pnd.read_csv(supply_path[:6] + "steal.csv", parse_dates = ["date"], index_col = "date")
stolen_summary_apple = stolen_summary.apple
stolen_summary_pen = stolen_summary.pen
stolen_summary_apple = stolen_summary_apple.groupby(key).sum()
stolen_summary_pen = stolen_summary_pen.groupby(key).sum()

temporary["year"] = apple_sold.index
strings = []
for iterate in apple_sold.index :
    strings.append(supply_path[:2])

temporary["state"] = strings
temporary["apple_sold"] = apple_sold.values
temporary["pen_sold"] = pen_sold.values
temporary["apple_stolen"] = stolen_summary_apple.values
temporary["pen_stolen"] = stolen_summary_pen.values

temporary.to_csv(supply_path[:6] + "temporary.csv", index = False)