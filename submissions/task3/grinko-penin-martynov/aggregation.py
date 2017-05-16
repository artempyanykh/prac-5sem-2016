import pandas as pnd
import os

shops = []

for filename in os.listdir(os.getcwd()):
    if "temporary.csv" in filename :
        shops.append(filename)

shops_list = []
for items in shops:
    shops_list.append(pnd.read_csv(items))

aggregation = pnd.concat(shops_list)
aggregation.groupby(["year", "state"]).sum().to_csv("Summary.csv", index = True)

for items in shops:
    os.remove(items)
