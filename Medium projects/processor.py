import numpy as np
from math import floor
from prettytable import PrettyTable


def create_matrix_from_input(noun: str = '') -> np.array:
	"""Creates a matrix from user input."""
	if noun == '':
		_n, _m = map(int, input('Enter matrix size: ').split())
		print(f'Enter matrix:')
	else:
		_n, _m = map(int, input(f'Enter size of {noun} matrix: ').split())
		print(f'Enter {noun} matrix:')

	matrix = []
	for _ in range(_n):
		line_in = input().split()
		line_var = []
		for c in line_in:
			try:
				line_var.append(int(c))
			except ValueError:
				line_var.append(float(c))
		matrix.append(line_var)
	return np.array(matrix)


def truncate(f, n):
	"""Return float in readable form"""
	return floor(f * 10 ** n) / 10 ** n


def print_matrix(matrix: np.array) -> None:
	"""Print matrix in readable form"""
	p = PrettyTable()
	for row in matrix:
		p.add_row(row)
	print(p.get_string(header=False, border=False))
	# print('\n'.join('   '.join(str(truncate(cell, 3)) for cell in row) for row in matrix))


def main():
	while True:
		print('1. Add matrices\n2. Multiply matrix by a constant\n3. Multiply matrices\n'
		      '4. Transpose matrix\n5. Calculate a determinant\n6. Inverse matrix\n0. Exit')
		choice: str = input('Your choice: ')
		if choice == '1' or choice == '3':
			m1 = create_matrix_from_input(noun='first')
			m2 = create_matrix_from_input(noun='second')
			if choice == '1':
				if len(m1) == len(m2) and len(m1[0]) == len(m2[0]):
					m1 = m1 + m2
				else:
					print('The operation cannot be performed.')
			else:
				if len(m1[0]) == len(m2):
					m1 = m1.dot(m2)
				else:
					print('The operation cannot be performed.')
			print('The result is:')
			print_matrix(m1)
		elif choice == '2':
			m1 = create_matrix_from_input(noun='first')
			constant = float(input('Enter constant: '))
			m1 = constant * m1
			print('The result is:')
			print_matrix(m1)
		elif choice == '4':
			choice = input('1. Main diagonal\n2. Side diagonal\n3. Vertical line\n'
			               '4. Horizontal line\nYour choice: ')
			m1 = create_matrix_from_input(noun='')
			if choice == '1':
				m1 = list(zip(*m1))
			elif choice == '2':
				m1 = list(zip(*[list(reversed(line)) for line in m1][-1::-1]))
			elif choice == '3':
				m1 = [list(reversed(line)) for line in m1]
			elif choice == '4':
				m1 = m1[-1::-1]
			print('The result is:')
			print_matrix(m1)
		elif choice == '5':
			m1 = create_matrix_from_input(noun='')
			print('The result is:')
			print(np.linalg.det(m1))
		elif choice == '6':
			m1 = create_matrix_from_input(noun='')
			print('The result is:')
			print_matrix(np.linalg.inv(m1))
		elif choice == '0':
			exit()
		else:
			print('Unexpected choice!')


if __name__ == '__main__':
	main()
