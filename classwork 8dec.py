#1
'''def sum_series(n):
    total = 0
    while n > 0:
        total += n
        n -= 2
    return total

# Test cases
print(sum_series(6))   # 12
print(sum_series(10))
'''
import math

#2
'''
def power(x, n):
    total = 1
    while n > 0:
        total *= x

print(pow(3,4))'''

#3
'''
class Person:
    def __init__(self, name, ID,group):
        self.name = name
        self.ID = ID
        self.group = group
        def __str__(self):
            return self.name + ' ' + self.ID + ' ' + self.group

gleb = Person('Gleb',1,'Computer Science')
print(gleb.name)
print(gleb.ID)
print(gleb.group)
print(gleb.__str__())
'''

#4
'''
class reverse_phrase:
    def __init__(self, phrase):
        words = phrase.split()
        norm_words = reversed(words)
        self.phrase = ' '.join(norm_words)
        rev = ' '.join(self.phrase.split()[::-1])

obj = reverse_phrase('computer science')
print(obj.phrase)   # science computer
'''

#5
'''
class get_string:
    def __init__(self, string):
        self.string = string
    def __str__(self):
        return self.string
class get1_string:
    def __init__(self, string):
        self.string = string
        print(self.string.upper())

print(get_string('computer science'))
get1_string('computer science')
'''

#6
'''
class rectangle:
    def __init__(self, width, length):
        self.width = width
        self.length = length
        print(length * width)
print(rectangle(6, 2))'''

#7
'''
def circle_area(radius):
    area = math.pi * radius ** 2
    print(area)
    perimeter = 2*math.pi*radius
    print(perimeter)
circle_area(6)'''

#8

print('register section ')
print('---------------------------------------')
class register:
    def __init__(self, name, password):
        self.name = name
        self.password = password

user1 = register(input('Enter username: '), input( 'Enter password: '))

print('register section done')
print('----------------------------------------------')
print('login section ')

class login:
    def __init__(self, name, password):
        self.name = name
        self.password = password

user1_login = login(input('Enter username: '), input('Enter password: '))

print('-----------------------------------------------')

if user1_login.name == user1.name and user1_login.password == user1.password:
        print('login success, congrats!')
else:
        print('login failed')
        exit()

class choose_options:
    def __init__(self, deposit, withdraw,show_balance,exit):
        self.deposit = deposit
        self.withdraw = withdraw
        self.show_balance = show_balance
        self.exit = exit
balance = 0
print('\n1. Deposit\n2. Withdraw\n3. Show Balance\n4. Exit \n')
choice =input('Enter your choice: ')
while True:



    if choice == 'deposit' or choice == '1':
        deposit = float(input('Enter deposit: '))
        balance+=deposit
        print('deposit success')
        choice =input('Enter your 2 choice: ')

    elif choice == 'withdraw' or choice == '2':
        withdraw = float(input('Enter withdraw: '))
        print('withdraw success')
        balance -= withdraw
        choice = input('Enter your 3 choice: ')

    elif choice == 'show balance' or choice == '3':
        print(balance)
        choice = input('Enter your 4 choice: ')

    elif choice == 'exit'or choice == '4':
        print('exit success')
        break
    else:
        print('invalid choice')


'''
class book:
    def __init__(atribute, title,author, ISBN, Quantity):
        atribute.title = title
        atribute.author = author
        atribute.ISBN = ISBN
        atribute.Quantity = Quantity

    def details(self,book_details, availability_check, update_quantity):
        

gleb = book(input('enter title: '),input('Enter author: '),input('Enter ISBN: '),input('Enter Quantity: '))
print(gleb.title, gleb.author, gleb.ISBN, gleb.Quantity ,gleb.book_details, end=' ')

class user:
    def __init__(attribute_user,name,ID,list_of_books_borrowed):
        attribute_user.name = name
        attribute_user.ID = ID
        attribute_user.list_of_books_borrowed = list_of_books_borrowed

    def __int__(methods_user, user_details,borrowed,returnbook):
        methods_user.user_details = user_details
        methods_user.borrowed = borrowed
        methods_user.returnbook = returnbook
        '''








