from random import sample, seed
import sqlite3


class BankingSystem:
    DB_file_name = 'card.s3db'
    DB_TABLE_name = 'card'
    DB_table_card_col_id = 'id'
    DB_table_card_col_number = 'number'
    DB_table_card_col_pin = 'pin'
    DB_table_card_col_balance = 'balance'

    def __init__(self):
        seed(1)
        self.database()

    def database(self, card=None, pin=None, balance=None) -> None:
        with sqlite3.connect(self.DB_file_name) as data:
            if not card:
                data.executescript(f'''
                    CREATE TABLE IF NOT EXISTS {self.DB_TABLE_name} (
                    {self.DB_table_card_col_id}         INTEGER     NOT NULL PRIMARY KEY AUTOINCREMENT,
                    {self.DB_table_card_col_number}     TEXT        NOT NULL UNIQUE,
                    {self.DB_table_card_col_pin}        TEXT        NOT NULL,
                    {self.DB_table_card_col_balance}    INTEGER     DEFAULT 0 NOT NULL
                    );
                    ''')
            else:
                cursor = data.cursor()
                cursor.execute(f'''
                    INSERT OR IGNORE INTO {self.DB_TABLE_name} (
                        {self.DB_table_card_col_number}, 
                        {self.DB_table_card_col_pin}, 
                        {self.DB_table_card_col_balance})
                    VALUES ({card}, {pin}, {balance});
                    ''')

    def check_credentials(self, card: str) -> str:
        with sqlite3.connect(self.DB_file_name) as data:
            cursor = data.cursor()
            cursor.execute(f'''
            SELECT {self.DB_table_card_col_pin} FROM {self.DB_TABLE_name}
            WHERE {self.DB_table_card_col_number} LIKE ({card});
            ''')
            return cursor.fetchone()

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
    def luhn_checksum(card_number: str) -> str or bool:
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

    def generate_numbers(self) -> tuple:
        while True:
            random_card: str = str(400_000) + ''.join([str(n) for n in sample(range(10), 9)])
            random_card += self.luhn_checksum(random_card)
            random_pin: str = ''.join([str(n) for n in sample(range(10), 4)])
            # check if card_number in database
            try:
                if self.check_credentials(random_card)[0]:
                    continue
            except TypeError:
                yield random_card, random_pin

    def create_account(self, card=None, pin=None, balance=0) -> None:
        rand_card, rand_pin = next(self.generate_numbers())
        if card is None:
            card = rand_card
        if pin is None:
            pin = rand_pin
        self.database(card, pin, balance)
        print('\nYour card has been created')
        print(f'Your card number:\n{card}')
        print(f'Your card PIN:\n{pin}\n')

    def do_transfer(self, card: str) -> None:
        to = input('Enter card number:\n')
        if card == to:
            print('You can\'t transfer money to the same account!\n')
        elif not self.luhn_checksum(to):
            print('You probably made a mistake in the card number. Please try again!\n')
        elif not self.check_credentials(to):
            print('Such card does not exist.\n')
        else:
            amount: str = input('Enter how much money you want to transfer:\n')
            if int(amount) > int(self.get_update(card)):
                print('Not enough money!\n')
            else:
                print(self.get_update(card, to, amount))

    def account(self, card: str) -> None:
        while True:
            choice: str = input('\n1. Balance\n2. Add income\n3. Do transfer\n4. Close account\n5. Log out\n0. Exit\n')
            if choice == '1':  # Balance
                print(f"\nBalance: {self.get_update(card)}\n")
            elif choice == '2':  # Add income
                income = int(input('Enter income:\n'))
                print(self.get_update(From=card, amount=income))
            elif choice == '3':  # Do transfer
                self.do_transfer(card)
            elif choice == '4':  # Close account
                print(self.get_update(From=card, close=True))
                return
            elif choice == '5':  # Log out
                print('You have successfully logged out.\n')
                return
            elif choice == '0':  # Exit
                print('Bye!')
                exit()
            else:
                print('Unknown option.\n')

    def login(self) -> None:
        card: str = input('Enter your card number:\n')
        pin: str = input('Enter your card PIN:\n')
        try:
            if self.check_credentials(card)[0] == pin:
                print('You have successfully logged in!')
                self.account(card)
            else:
                print('Wrong card number or PIN')
        except TypeError:
            print('Wrong card number or PIN')

    def get_update(self, From=None, to=None, amount=None, close=False) -> str:
        with sqlite3.connect('card.s3db') as data:
            cur = data.cursor()
            if From and to:
                cur.execute(f'''
                UPDATE {self.DB_TABLE_name}
                SET {self.DB_table_card_col_balance} = ({self.DB_table_card_col_balance} + {amount}) 
                WHERE {self.DB_table_card_col_number} LIKE {to};
                ''')
                cur.execute(f'''
                UPDATE {self.DB_TABLE_name}
                SET {self.DB_table_card_col_balance} = ({self.DB_table_card_col_balance} - {amount}) 
                WHERE {self.DB_table_card_col_number} LIKE {From};
                ''')
                return 'Success!'
            elif From and amount:
                cur.execute(f'''
                UPDATE {self.DB_TABLE_name} 
                SET {self.DB_table_card_col_balance} = ({self.DB_table_card_col_balance} + {amount}) 
                WHERE number LIKE {From};
                ''')
                return 'Income was added!'
            elif close:
                cur.execute(f'''
                DELETE FROM {self.DB_TABLE_name} 
                WHERE {self.DB_table_card_col_number} = {From};
                ''')
                return 'The account has been closed!\n'
            else:
                cur.execute(f'''
                    SELECT {self.DB_table_card_col_balance} FROM {self.DB_TABLE_name} 
                    WHERE {self.DB_table_card_col_number} LIKE {From};''')
                # return account balance
                return cur.fetchone()[0]


BankingSystem().menu()
