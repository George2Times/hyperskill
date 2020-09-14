import unittest
import hack


class MyTestCase(unittest.TestCase):
	def test_password_generator(self):
		gen = hack.password_generator(alphabet=' ', length=1)
		for i, g in enumerate(gen):
			print(i, g, sep=')')


	def test_login_password_to_json_str(self):
		self.assertEqual(hack.login_password_to_json_str(' '),
		                 '{"login": " ", "password": " "}')
		self.assertEqual(hack.login_password_to_json_str('admin'),
		                 '{"login": "admin", "password": " "}')
		self.assertEqual(hack.login_password_to_json_str('admin', ' '),
		                 '{"login": "admin", "password": " "}')
		self.assertEqual(hack.login_password_to_json_str('admin', 'abc'),
		                 '{"login": "admin", "password": "abc"}')

	def test_json_str_to_py_object(self):
		self.assertEqual(hack.json_str_to_py_object('{"login": " ", "password": " "}'),
		                 {"login": " ", "password": " "})
		self.assertEqual(hack.json_str_to_py_object('{"login": "admin", "password": " "}'),
		                 {"login": "admin", "password": " "})
		self.assertEqual(hack.json_str_to_py_object('{"login": "admin", "password": " "}'),
		                 {"login": "admin", "password": " "})
		self.assertEqual(hack.json_str_to_py_object('{"login": "admin", "password": "abc"}'),
		                 {"login": "admin", "password": "abc"})




if __name__ == '__main__':
	unittest.main()
