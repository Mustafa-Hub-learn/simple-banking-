import random
import sqlite3
conn = sqlite3.connect('card.s3db')
cur = conn.cursor()

#Create a table
cur.execute("""CREATE TABLE IF NOT EXISTS card (
id INTEGER PRIMARY KEY AUTOINCREMENT,
number TEXT,
pin TEXT,
balance INTEGER DEFAULT 0); """)
conn.commit()

#Get all details from table and store as details


login_menu = """1. Create an account
2. Log into account
0. Exit"""

logged_in = False

logged_in_menu = """1. Balance
2. Add income
3. Do transfer
4. Close account
5. Log out
0. Exit """


class CreditCard:
    def __init__(self):
        self.card_number = None
        self.card_pin = None

    def generate_card(self):
        placeholder = 400000000000000 + random.randint(0, 999999999)

        def luhncc(n):
            #takes the digits of an input and returns as a list
            def digits_of_cc(n):
                return [int(d) for d in str(n)]
            digits = digits_of_cc(placeholder)
            odd_digits = digits[0::2]
            even_digits = digits[1::2]
            checksum = 0
            checksum += sum(even_digits)
            for dig in odd_digits:
                checksum += sum(digits_of_cc(dig * 2))
            if checksum % 10 == 0:
                return 0
            else:
                return 10 - (checksum % 10)
        self.card_number = int(str(placeholder) + str(luhncc(placeholder)))
        self.card_pin = random.randint(1000, 9999)
        cur.execute("""INSERT INTO card (number, pin) VALUES ({0},{1})""".format(self.card_number, self.card_pin))
        conn.commit()
        print("Your card has been created")
        print("Your card number is:")
        print(self.card_number)
        print("Your pin is:")
        print(self.card_pin)
        print("")


def luhn_check(n):
    def digits_of(n):
        return[int(item) for item in str(n)]
    card = digits_of(n)
    checksum = card[-1]
    card.pop()
    odd = card[0::2]
    even = card[1::2]
    total = 0
    total += sum(even)
    for dig in odd:
        checksum += sum(digits_of(dig * 2))
    if (total + checksum) % 10 == 0:
        return True
    else:
        return False


mycard = CreditCard()

print(login_menu)
while not logged_in:
    user_selection = int(input())
    if user_selection == 1:
        mycard.generate_card()
        print(login_menu)
    elif user_selection == 2:
        cur.execute("""SELECT * FROM card""")
        details = cur.fetchall()
        print("Enter your card number:")
        card_number = int(input())
        print("Enter your PIN:")
        PIN = int(input())
        card_exists = False
        for item in details:
            if str(card_number) in item and str(PIN) in item:
                card_exists = True
        if card_exists:
            print("You have successfully logged in!")
            print("")
            print(logged_in_menu)
            logged_in = True
            break
        elif not card_exists:
            print("Wrong card number or PIN!")
            print("")
            print(login_menu)
    elif user_selection == 0:
        print("Bye!")
        break

while logged_in:
    card_number = str(card_number)
    user_input = int(input())
    if user_input == 1:
        cur.execute("""SELECT balance FROM card WHERE number = {0};""".format(card_number))
        balance = cur.fetchall()[0][0]
        print("Balance: " + str(balance))
        print("")
        print(logged_in_menu)
        #Check balance(pull balance from table)
    elif user_input == 2:
        print("Enter income:")
        income_amount = int(input())
        cur.execute("""UPDATE card SET balance=(balance+{0}) WHERE number={1};""".format(income_amount, card_number))
        print("Income was added!")
        print("")
        print(logged_in_menu)
        #Add income(add money to account)
    elif user_input == 3:
        cur.execute("""SELECT * FROM card""")
        details = cur.fetchall()
        print("Enter a card number:")
        money_destination = input()
        if not luhn_check(money_destination):
            print("Probably you made a mistake in the card number. Please try again!")
            print(logged_in_menu)
        else:
            destination_exists = False
            for item in details:
                if money_destination in item:
                    destination_exists = True
            if not destination_exists:
                print("Such a card does not exist")
                print("")
                print(logged_in_menu)
            else:
                transfer_amount = int(input())
                if transfer_amount > int(balance):
                    print("Not enough money!")
                    print("")
                    print(logged_in_menu)
                else:
                    cur.execute("""UPDATE card SET balance=(balance-{0}) WHERE number={1};
UPDATE card SET balance=(balance+{0}) WHERE number={2}; """.format(transfer_amount, card_number, money_destination))
                    conn.commit()
                    print("Success!")
        #transfer Money(take money from one account add to another)
    elif user_input == 4:
        cur.execute("""DELETE FROM card WHERE number={0}""".format(card_number))
        conn.commit()
        print("The account has been closed!")
        print("")
        print(login_menu)
        logged_in = False
        break
        #Close account(delete values from table)
    elif user_input == 5:
        print("You have successfully logged out!")
        logged_in = False
        print("")
        print(login_menu)
        #log out(logged in == false)
    elif user_input == 0:
        print("Bye!")
        break
        #exit(break)
