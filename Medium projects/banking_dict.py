from random import sample, seed


class BankingSystem:
	def __init__(self):
		self.cards: dict = dict()
		seed(1)

	def menu(self) -> None:
		while True:
			choice: str = input("\n1. Create an account\n2. Log into account\n0. Exit\n")
			if choice == '1':
				self.create_account()
			elif choice == '2':
				self.login()
			elif choice == '0':
				print('Bye!')
				exit()
			else:
				print('Unknown option.')

	# Return checksum of Luhn algorithm
	# or True/False if checksum is correct
	@staticmethod
	def Luhn_checksum(card_number: str) -> str or bool:
		if len(card_number) not in (15, 16):
			return 'Invalid length'

		numbers = list(map(int, [char for char in card_number[0:15]]))
		for i in range(0, len(numbers), 2):
			numbers[i] *= 2
			if numbers[i] > 9:
				numbers[i] -= 9

		if len(card_number) == 15:
			return str((10 - sum(numbers) % 10) % 10)
		else:
			return (sum(numbers) + int(card_number[15])) % 10 == 0

	# Generate card numbers and pins
	@classmethod
	def generate_numbers(cls) -> tuple:
		while True:
			random_card: str = str(400_000) + ''.join([str(n) for n in sample(range(10), 9)])
			random_card += cls.Luhn_checksum(random_card)
			random_pin: str = ''.join([str(n) for n in sample(range(10), 4)])
			yield random_card, random_pin

	def create_account(self) -> None:
		card, pin = next(self.generate_numbers())
		self.cards[card] = {'PIN': pin, 'Balance': 0}
		print('Your card has been created')
		print(f'Your card number:\n{card}')
		print(f'Your card PIN:\n{pin}')

	def get_balance(self, card) -> int:
		return self.cards[card]["Balance"]

	def add_income(self, card: str) -> None:
		income = int(input('Enter income:\n'))
		self.cards[card]["Balance"] += income
		print('Income was added!')

	def do_transfer(self, card) -> None:
		print(self.cards)
		destination = input('Transfer\nEnter card number:\n')
		if not self.Luhn_checksum(destination):
			print('Probably you made a mistake in the card number. Please try again!')
		elif self.cards.get(destination) is None:
			print('Such a card does not exist.')
		elif card == destination:
			print("You can't transfer money to the same account!")
		else:
			amount = int(input('Enter how much money you want to transfer:\n'))
			if amount > self.cards[card]["Balance"]:
				print('Not enough money!')
			else:
				self.cards[card]["Balance"] -= amount
				self.cards[destination]["Balance"] += amount
				print('Success!')

	def account(self, card: str) -> None:
		while True:
			choice: str = input('''
1. Balance
2. Add income
3. Do transfer
4. Close account
5. Log out
0. Exit
''')
			if choice == '1':  # Balance
				print(f'Balance: {self.get_balance(card)}')
			elif choice == '2':  # Add income
				self.add_income(card)
			elif choice == '3':  # Do transfer
				self.do_transfer(card)
			elif choice == '4':  # Close account
				print('The account has been closed!')
				del self.cards[card]
				return
			elif choice == '5':  # Log out
				print('You have successfully logged out!')
				return
			elif choice == '0':  # Exit
				print('Bye!')
				exit()
			else:
				print('Unknown option.')

	def login(self) -> None:
		card: str = input('Enter your card number:\n')
		pin: str = input('Enter your card PIN:\n')
		try:
			if self.cards[card]['PIN'] == pin:
				print('You have successfully logged in!')
				self.account(card)
			else:
				print('Wrong card number or PIN')
		except KeyError:
			print('Wrong card number or PIN')


BankingSystem().menu()
# print(BankingSystem.Luhn_checksum('400000844943340'))
