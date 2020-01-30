import random

options_default = ('rock', 'scissors', 'paper')
# options = ('rock', 'gun', 'lightning', 'devil', 'dragon',
#            'water', 'air', 'paper', 'sponge', 'wolf',
#            'tree', 'human', 'snake', 'scissors', 'fire')
#
# options_win = {'rock': ['fire', 'scissors', 'snake', 'human', 'tree', 'wolf', 'sponge'],
#                'fire': ['paper', 'scissors', 'snake', 'human', 'tree', 'wolf', 'sponge'],
#                'scissors': ['paper', 'air', 'snake', 'human', 'tree', 'wolf', 'sponge'],
#                'snake': ['paper', 'air', 'water', 'human', 'tree', 'wolf', 'sponge'],
#                'human': ['paper', 'air', 'water', 'dragon', 'tree', 'wolf', 'sponge'],
#                'tree': ['paper', 'air', 'water', 'dragon', 'devil', 'wolf', 'sponge'],
#                'wolf': ['paper', 'air', 'water', 'dragon', 'devil', 'lightning', 'sponge'],
#                'sponge': ['paper', 'air', 'water', 'dragon', 'devil', 'lightning', 'gun'],
#                'paper': ['air', 'water', 'dragon', 'devil', 'lightning', 'gun', 'rock'],
#                'air': ['water', 'dragon', 'devil', 'lightning', 'gun', 'rock', 'fire'],
#                'water': ['dragon', 'devil', 'lightning', 'gun', 'rock', 'fire', 'scissors'],
#                'dragon': ['devil', 'lightning', 'gun', 'rock', 'fire', 'scissors', 'snake'],
#                'devil': ['lightning', 'gun', 'rock', 'fire', 'scissors', 'snake', 'human'],
#                'lightning': ['gun', 'rock', 'fire', 'scissors', 'snake', 'human', 'tree'],
#                'gun': ['rock', 'fire', 'scissors', 'snake', 'human', 'tree', 'wolf'],
#                }

if __name__ == '__main__':
	user_rating = 1350
	user_name = input('Enter your name: ')
	print(f'Hello, {user_name}')

	user_options = input()
	# numbers of options must be odd
	if user_options == '':
		options = options_default
	else:
		options = user_options.split(',')
		options[1:] = options[len(options):0:-1]

	win_degree = (len(options) - 1) / 2
	print("\nOkay, let's start")
	while True:
		user_choice = input()
		computer_choice = random.choice(options)
		# if user_choice == '':
		# 	user_choice = random.choice(options_default)
		if user_choice == '!help':
			print('Help')
		elif user_choice == '!exit':
			print('Bye!')
			break
		elif user_choice == '!rating':
			print(f'Your rating: {user_rating}')
		elif user_choice in options:
			result = (options.index(computer_choice) - options.index(user_choice)) % len(options)
			# Draw
			if computer_choice == user_choice:
				print(f'There is a draw ({computer_choice})')
				user_rating += 50
			# Win
			elif result <= win_degree:
				print(f'Well done. Computer chose {computer_choice} and failed')
				user_rating += 100
			# Lose
			else:
				print(f'Sorry, but computer chose {computer_choice}')
				# user_rating -= 100
		else:
			print('Wrong choice:', user_choice)

