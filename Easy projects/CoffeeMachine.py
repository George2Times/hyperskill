

class CoffeeMachine:

	def __init__(self, money, water, milk, coffee_beans, disposable_cups):
		self.water = water
		self.milk = milk
		self.coffee_beans = coffee_beans
		self.disposable_cups = disposable_cups
		self.money = money

	def print_self(self):
		print(
			'The coffee machine has:\n',
			'{} of water\n'.format(self.water),
			'{} of milk\n'.format(self.milk),
			'{} of coffee beans\n'.format(self.coffee_beans),
			'{} of disposable cups\n'.format(self.disposable_cups),
			'${} of money'.format(self.money) if self.money > 0 else '{} of money'.format(self.money)
		)
		return None

	def buy(self):
		what = input('What do you want to buy? 1 - espresso, 2 - latte, 3 - cappuccino: ')
		if what == 'espresso' or what == '1':
			if self.water >= 250:
				if self.coffee_beans >= 16:
					if self.disposable_cups >= 1:
						self.water = self.water - 250
						self.coffee_beans = self.coffee_beans - 16
						self.disposable_cups = self.disposable_cups - 1
						self.money = self.money + 4
						print('I have enough resources, making you a espresso!')
				else:
					print('Sorry, not enough coffee beans!')
			else:
				print('Sorry, not enough water!')
		elif what == 'latte' or what == '2':
			if self.water >= 350:
				if self.milk >= 75:
					if self.coffee_beans >= 20:
						if self.disposable_cups >= 1:
							self.water = self.water - 350
							self.milk = self.milk - 75
							self.coffee_beans = self.coffee_beans - 20
							self.disposable_cups = self.disposable_cups - 1
							self.money = self.money + 7
							print('I have enough resources, making you a latte!')
					else:
						print('Sorry, not enough coffee beans!')
				else:
					print('Sorry, not enough milk!')
			else:
				print('Sorry, not enough water!')
		elif what == 'cappuccino' or what == '3':
			if self.water >= 200:
				if self.milk >= 100:
					if self.coffee_beans >= 12:
						if self.disposable_cups >= 1:
							self.water = self.water - 200
							self.milk = self.milk - 100
							self.coffee_beans = self.coffee_beans - 12
							self.disposable_cups = self.disposable_cups - 1
							self.money = self.money + 6
							print('I have enough resources, making you a cappuccino!')
					else:
						print('Sorry, not enough coffee beans!')
				else:
					print('Sorry, not enough milk!')
			else:
				print('Sorry, not enough water!')
		elif what == 'back':
			return None
		else:
			print('Unknown command')
		return None

	def take(self):
		print("I gave you $%s" % self.money)
		self.money = 0
		return None

	def fill(self):
		a = int(input("Write how many ml of water do you want to add: "))
		self.water = self.water + a
		a = int(input("Write how many ml of milk do you want to add: "))
		self.milk = self.milk + a
		a = int(input("Write how many grams of coffee beans do you want to add: "))
		self.coffee_beans = self.coffee_beans + a
		a = int(input("Write how many disposable cups of coffee do you want to add: "))
		self.disposable_cups = self.disposable_cups + a
		return None

	def remaining(self):
		self.print_self()


def main():
	coffee_machine_1 = CoffeeMachine(money=550, water=400, milk=540, coffee_beans=120, disposable_cups=9)
	while True:
		action = input('Write action (buy, fill, take, remaining, exit): ')
		if action == 'buy':
			coffee_machine_1.buy()
		elif action == 'fill':
			coffee_machine_1.fill()
		elif action == 'take':
			coffee_machine_1.take()
		elif action == 'remaining':
			coffee_machine_1.remaining()
		elif action == 'exit':
			break
		else:
			print('Unknown action')
		print()


if __name__ == '__main__':
	main()
