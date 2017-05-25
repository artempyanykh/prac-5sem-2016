import sys, re
from os import listdir
from os.path import isfile, join

# main entity
class GoodsState:
	def __init__(self, date='', quantity_apple=0, quantity_pen=0):
		self.date = date
		self.quantity_apple = quantity_apple
		self.quantity_pen = quantity_pen


	def from_string(self, string):
		values = string.rstrip().split(',')
		self.date = values[0]
		self.quantity_apple = int(values[1])
		self.quantity_pen = int(values[2])
		return self


	def __str__(self):
		return self.date + ',' + str(self.quantity_apple) + ',' + str(self.quantity_pen) + '\n'


	def __add__(self, other):
		result = GoodsState(date=self.date)
		result.quantity_apple = self.quantity_apple + other.quantity_apple
		result.quantity_pen = self.quantity_pen + other.quantity_pen
		return result


	def __sub__(self, other):
		result = GoodsState(date=self.date)
		result.quantity_apple = self.quantity_apple - other.quantity_apple
		result.quantity_pen = self.quantity_pen - other.quantity_pen
		return result


# help function to iterate through sells
def get_next_transaction(iterable):
	it = iter(iterable)
	current = next(it)
	current_date = current[:10]
	current_type = current[17]

	try:
		while True:
			following = next(it)
			following_date = following[:10]
			following_type = following[17]

			yield following_date, current_type, current_date != following_date

			current_date = following_date
			current_type = following_type
	except:
		yield '', current_type, True


# generates daily and steal statistics
def get_data(shop):
	# parse supply
	supply = []
	with open(shop + '-supply.csv') as file:
		next(file)
		for line in file:
			supply.append(GoodsState().from_string(line))
	supply_count = len(supply)

	#parse inventory states
	inventory_states = []
	with open(shop + '-inventory.csv') as file:
		next(file)
		for line in file:
			inventory_states.append(GoodsState().from_string(line))
	inventory_states_count = len(inventory_states)

	# create daily and steal statistics
	daily = []
	steal = []
	sold = []
	with open(shop + '-sell.csv') as file:
		next(file)

		last_supply_id = 0
		current_state = GoodsState(date=supply[last_supply_id].date)
		day_sales = GoodsState(date=supply[last_supply_id].date)
		
		last_inventory_state_id = 0
		
		for next_date, transaction_product, date_will_change in get_next_transaction(file):
			if transaction_product == 'a':
				day_sales.quantity_apple += 1
			else:
				day_sales.quantity_pen += 1

			if date_will_change:
				current_state -= day_sales

				if last_supply_id < supply_count and current_state.date == supply[last_supply_id].date:
					current_state += supply[last_supply_id]
					last_supply_id += 1

				if last_inventory_state_id < inventory_states_count and current_state.date == inventory_states[last_inventory_state_id].date:
					steal.append(current_state - inventory_states[last_inventory_state_id])
					current_state = inventory_states[last_inventory_state_id]
					last_inventory_state_id += 1

				sold.append(GoodsState(day_sales.date, day_sales.quantity_apple, day_sales.quantity_pen))
				daily.append(GoodsState(current_state.date, current_state.quantity_apple, current_state.quantity_pen))
				day_sales = GoodsState(date=next_date)
				current_state.date = next_date
	return daily, steal, sold
	

def process_data(shop, steal, sold):
	data = []

	with open(shop + '-steal.csv', 'w') as file_steal:
		file_steal.write('date,apple,pen\n')

		current_year_sold = GoodsState(date=sold[0].date[:4])
		current_year_stolen = GoodsState(date=sold[0].date[:4])

		last_steal_id = 0
		steal_count = len(steal)
		sold_count = len(sold)

		for i in range(sold_count):
			current_year_sold += sold[i]
			if last_steal_id < steal_count and steal[last_steal_id].date == sold[i].date:
				current_year_stolen += steal[last_steal_id]
				file_steal.write(str(steal[last_steal_id]))
				last_steal_id += 1

			try:
				if sold[i + 1].date[:4] != current_year_sold.date:
					raise
			except:
				data.append((current_year_sold.date, current_year_sold.quantity_apple, current_year_stolen.quantity_apple, current_year_sold.quantity_pen, current_year_stolen.quantity_pen))
				if i < sold_count - 1:
					current_year_sold = GoodsState(date=sold[i + 1].date[:4])
					current_year_stolen = GoodsState(date=sold[i + 1].date[:4])

	return data


# main entry
def main(argv):
	argv.append('./') # for tests

	if len(argv) < 2:
		print 'task3\nUsage:\n\tpython ' + argv[0] + ' FOLDER1 [FOLDER2 [...]]\n'
	else:
		agregate_data = {}
		for folder in argv[1:]:
			files = [f for f in listdir(folder) if isfile(join(folder, f))]


			is_file_supply = r"([\w]+)-([\w]+)-supply\.csv"
			for file in files:
				m = re.match(is_file_supply, file)
				if m:
					state = m.groups()[0]
					shop = join(folder, state + '-' + m.groups()[1])

					daily, steal, sold = get_data(shop)

					with open(shop + '-daily.csv', 'w') as file_daily:
						file_daily.write('date,apple,pen\n')
						for daily_state in daily:
							file_daily.write(str(daily_state))

					data = process_data(shop, steal, sold)
					for row in data:
						if not row[0] in agregate_data:
							agregate_data[row[0]] = {state: (row[1], row[2], row[3], row[4])}
						else:
							if state in agregate_data[row[0]]:
								last_row = agregate_data[row[0]][state]
								agregate_data[row[0]][state] = (last_row[0] + row[1], last_row[1] + row[2], last_row[2] + row[3], last_row[3] + row[4])
							else:
								agregate_data[row[0]][state] = (row[1], row[2], row[3], row[4])

		with open('agregate.csv', 'w') as file_agregate:
			file_agregate.write('year,state,apple_sold,apple_stolen,pen_sold,pen_stolen\n')
			for year, states in agregate_data.iteritems():
				for state, data in states.iteritems():
					file_agregate.write(year + ',' + state + ',' + str(data[0]) + ',' + str(data[1]) + ',' + str(data[2]) + ',' + str(data[3]) + '\n')


main(sys.argv)