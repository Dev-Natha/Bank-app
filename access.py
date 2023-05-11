import sys
import re
import time
import random
import mysql.connector as connection
myconn = connection.connect(host = "127.0.0.1", user = "root", passwd = "ayilara10maranatha30", database = "bank_app")
cursor= myconn.cursor()


def welcome():
    print("""
    Welcome to Access Banking App. Which of the following operations would you like to perform?
    1) Log in to my Account
    2) Register a new account
    3) Deposit Cash
    4) Quit""")
    answer = input(">>> ")
    if answer == "1":
        login()
    elif answer == "2":
        registration()
    elif answer == "3":
        adminOperation()
    elif answer == "4":
        sys.exit()
    else:
        print("Invalid input. Try again")
        welcome()
        
def registration():
    myquery = "INSERT INTO access(first_name, last_name, user_name, age, address, account_type, account_number, account_balance, phone_number, network, passwd, confirmpasswd) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    first_name = input("Enter your first name ")
    last_name = input("Enter your last name ")
    age = input("Enter your Age ") 
    checkEmail()
    checkNumber()
    address = input("Enter your Address ")
    print("""Choose the type of account you want to create
    1. Savings Account
    2. Current Account
    3. Domicilliary Account""")
    account_type = input(">>> ")
    if account_type == "1":
        account_type = "Savings"
    elif account_type == "2":
        account_type = "Current"
    elif account_type == "3":
        account_type = "Domicilliary"
    else:
        account_type = "Savings"
    checkPassword()
    account_number = random.randrange(1533460001, 1533899999)
    values = (first_name, last_name, email, age, address, account_type, account_number, 0, phone_number, network, password, confirm_password)
    cursor.execute(myquery, values)
    myconn.commit()
    query = "SELECT * from access where passwd =%s and user_name =%s"
    val = (password, email)
    cursor.execute(query, val)
    result = cursor.fetchone()
    if result:
        time.sleep(2)
        print(f"Hello {result[1]}, your registration is successful and your account number is {result[7]}")
        print("Input 1 to go log in and 2 to go back home")
        response = input(">>> ")
        while True:
            if response == "1":
                login()
                break
            elif response == "2":
                welcome()
                break
            else:
                response = input("Invalid Input. Try again >>> ")
    else:
        print("Something went wrong with your registration")
    

def checkEmail():
    global email
    email = input("Enter your email ")
    check_email = re.findall(r"^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$", email)
    if not check_email:
        print("Invalid email. Try again")
        time.sleep(1)
        checkEmail()  
    else:
        return

def checkNumber():
    global phone_number
    global network
    phone_number = input("Enter your phone number ")
    Airtel = ("0802", "0808", "0708", "0812", "0701", "0902", "0901", "0904", "0907", "0912")
    MTN = ("0803", "0806", "0703", "0706", "0813", "0816", "0810", "0814", "0903", "0906", "0913", "0916", "0705", "07026", "0704")
    GLO = ("0805", "0807", "0705", "0815", "0811", "0905", "0915")
    Etisalat =  ("0809", "0818", "0817", "0909","0908")
    if not phone_number.isdigit() or len(phone_number) != 11:
        print("Input a valid phone number")
        checkNumber()
    else:
        if phone_number.startswith(Airtel):
            network = "Airtel"
        elif phone_number.startswith(MTN):
            network = "MTN"
        elif phone_number.startswith(GLO):
            network = "GLO"
        elif phone_number.startswith(Etisalat):
            network = "9Mobile"
        else:
            network = "N/A"
        return
def checkPassword():
    global password
    global confirm_password
    password = input("Enter your Password ")
    if not password.isdigit() or len(password) <= 3:
        print("Password must be 4 or more digits")
        checkPassword()
    else:
        confirm_password = input("Confirm your Password ")
        if password != confirm_password:
            print("Password does not match. Try again")
            checkPassword()
        else:
            return 

def login():
    global login_username
    global login_password
    login_username = input("Enter your email ")
    login_password = input("Enter your password ")
    try:
        query = "SELECT * from access where passwd =%s and user_name =%s"
        val = (login_password, login_username)
        cursor.execute(query, val)
        login_result = cursor.fetchone()
        if login_username == login_result[3] and login_password == str(login_result[11]):
            mainMenu()
    except TypeError:
        print("Invalid details")
        print("""Input 1 to try again and 2 to go back home""")
        user_input = input(">>> ")
        while True:
            if user_input == "1":
                login()
                break
            elif user_input == "2":
                welcome()
                break
            else:
                user_input = input("Invalid Input. Try again >>> ")

def mainMenu():
    query = "SELECT * from access where passwd =%s and user_name =%s"
    val = (login_password, login_username)
    cursor.execute(query, val)
    login_result = cursor.fetchone()
    print(f"Welcome {login_result[1]} {login_result[2]}. Which of the following banking operations would you like to perform")
    print("""
    1. Check Balance
    2. Transfer
    3. Buy Airtime
    4. Cables and Subscription
    5. Log out
    6. Reset Password
    """)
    response = input(">>> ")
    if response == "1":
        checkBalance()
    elif response == "2":
        transfer()
    elif response == "3":
        buyAirtime()
    elif response == "4":
        cables()
    elif response == "5":
        welcome()
    elif response == "6":
        reset()
    else:
        print("Invalid input")
        mainMenu()


def checkBalance():
    query = "SELECT * from access where passwd =%s and user_name =%s"
    val = (login_password, login_username)
    cursor.execute(query, val)
    login_result = cursor.fetchone()
    print(f"Your account balance is #{login_result[8]}.00 naira")
    print("Input 1 to go to the main menu and 2 to log out")
    response = input(">>> ")
    while True:
        if response == "1":
            mainMenu()
            break
        elif response == "2":
            welcome()
            break
        else:
            response = input("Invalid Input. Try again >>> ")


def transfer():
    bank_name = input("Enter recipient's bank name ").lower()
    if bank_name == "access":
        accessTransfer()
    elif bank_name == "polaris":
        polarisTransfer()
    elif bank_name == "zenith":
        zenithTransfer()
    else:
        print("We currently don't have that bank reigstered with us. You can choose either 'Access', 'Polaris' or 'Zenith'")
        transfer()


def accessTransfer():
    try:
        account_num = int(input(("Enter recipient's account number ")))
        query = "SELECT * from access where account_number =%s"
        val = (account_num, )
        cursor.execute(query, val)
        result = cursor.fetchone()
        if result == None:
            print("Account number does not exist")
            accessTransfer()
        else:
            try:
                amount = int(input("Enter the amount you want to transfer "))
                query = "SELECT * from access where passwd =%s and user_name =%s"
                val = (login_password, login_username)
                cursor.execute(query, val)
                login_result = cursor.fetchone()
                balance = login_result[8]
                if balance < amount:
                    print("You do not have sufficient balance to make this transfer")
                    print("Input 1 to go to the main menu and 2 to log out")
                    response = input(">>> ")
                    while True:
                        if response == "1":
                            mainMenu()
                            break
                        elif response == "2":
                            welcome()
                            break
                        else:
                            response = input("Invalid Input. Try again >>> ")
                else:
                    new_amount = balance - amount
                    val2 = (new_amount, login_result[0])
                    myquery = "UPDATE access SET account_balance =%s where id =%s"
                    cursor.execute(myquery, val2)
                    myconn.commit()
                    recipientBal = amount + result[8]
                    query2 = "UPDATE access SET account_balance =%s where account_number =%s"
                    val3 = (recipientBal, account_num)
                    cursor.execute(query2, val3)
                    myconn.commit()
                    print("Please wait")
                    time.sleep(2)
                    print(f"You have successfully transferred {amount} naira to {result[1]} {result[2]}")
                    print("Input 1 to go to the main menu and 2 to log out")
                    response = input(">>> ")
                    while True:
                        if response == "1":
                            mainMenu()
                            break
                        elif response == "2":
                            welcome()
                            break
                        else:
                            response = input("Invalid Input. Try again >>> ")
            except ValueError:
                print("Amount must be in digits. Try again")
                accessTransfer()
    except ValueError:
        print("Invalid Account Number")
        accessTransfer()

 
def polarisTransfer():
    try:
        account_num = int(input(("Enter recipient's account number ")))
        query = "SELECT * from polaris where account_number =%s"
        val = (account_num, )
        cursor.execute(query, val)
        result = cursor.fetchone()
        if result == None:
            print("Account number does not exist")
            polarisTransfer()
        else:
            try:
                amount = int(input("Enter the amount you want to transfer "))
                query = "SELECT * from access where passwd =%s and user_name =%s"
                val = (login_password, login_username)
                cursor.execute(query, val)
                login_result = cursor.fetchone()
                balance = login_result[8]
                if balance < amount:
                    print("You do not have sufficient balance to make this transfer")
                    print("Input 1 to go to the main menu and 2 to log out")
                    response = input(">>> ")
                    while True:
                        if response == "1":
                            mainMenu()
                            break
                        elif response == "2":
                            welcome()
                            break
                        else:
                            response = input("Invalid Input. Try again >>> ")
                else:
                    charges = 10
                    new_amount = (balance - amount) - charges
                    val2 = (new_amount, login_result[0])
                    myquery = "UPDATE access SET account_balance =%s where id =%s"
                    cursor.execute(myquery, val2)
                    myconn.commit()
                    recipientBal = amount + result[9]
                    query2 = "UPDATE polaris SET account_balance =%s where account_number =%s"
                    val3 = (recipientBal, account_num)
                    cursor.execute(query2, val3)
                    myconn.commit()
                    print("Please wait")
                    time.sleep(2)
                    print(f"You have successfully transferred {amount} naira to {result[1]} {result[2]}")
                    print("Input 1 to go to the main menu and 2 to log out")
                    response = input(">>> ")
                    while True:
                        if response == "1":
                            mainMenu()
                            break
                        elif response == "2":
                            welcome()
                            break
                        else:
                            response = input("Invalid Input. Try again >>> ")
            except ValueError:
                print("Amount must be in digits. Try again")
                polarisTransfer()
    except ValueError:
        print("Invalid Account Number")
        polarisTransfer()


def zenithTransfer():
    try:
        account_num = int(input(("Enter recipient's account number ")))
        query = "SELECT * from zenith where account_number =%s"
        val = (account_num, )
        cursor.execute(query, val)
        result = cursor.fetchone()
        if result == None:
            print("Account number does not exist")
            zenithTransfer()
        else:
            try:
                amount = int(input("Enter the amount you want to transfer "))
                query = "SELECT * from access where passwd =%s and user_name =%s"
                val = (login_password, login_username)
                cursor.execute(query, val)
                login_result = cursor.fetchone()
                balance = login_result[8]
                if balance < amount:
                    print("You do not have sufficient balance to make this transfer")
                    print("Input 1 to go to the main menu and 2 to log out")
                    response = input(">>> ")
                    while True:
                        if response == "1":
                            mainMenu()
                            break
                        elif response == "2":
                            welcome()
                            break
                        else:
                            response = input("Invalid Input. Try again >>> ")
                else:
                    charges = 10
                    new_amount = (balance - amount) - charges
                    val2 = (new_amount, login_result[0])
                    myquery = "UPDATE access SET account_balance =%s where id =%s"
                    cursor.execute(myquery, val2)
                    myconn.commit()
                    recipientBal = amount + result[9]
                    query2 = "UPDATE zenith SET account_balance =%s where account_number =%s"
                    val3 = (recipientBal, account_num)
                    cursor.execute(query2, val3)
                    myconn.commit()
                    print("Please wait")
                    time.sleep(2)
                    print(f"You have successfully transferred {amount} naira to {result[1]} {result[2]}")
                    print("Input 1 to go to the main menu and 2 to log out")
                    response = input(">>> ")
                    while True:
                        if response == "1":
                            mainMenu()
                            break
                        elif response == "2":
                            welcome()
                            break
                        else:
                            response = input("Invalid Input. Try again >>> ")
            except ValueError:
                print("Amount must be in digits. Try again")
                zenithTransfer()
    except ValueError:
        print("Invalid Account Number")
        zenithTransfer()


def buyAirtime():
    try:
        Airtel = ("0802", "0808", "0708", "0812", "0701", "0902", "0901", "0904", "0907", "0912")
        MTN = ("0803", "0806", "0703", "0706", "0813", "0816", "0810", "0814", "0903", "0906", "0913", "0916", "0705", "07026", "0704")
        GLO = ("0805", "0807", "0705", "0815", "0811", "0905", "0915")
        Etisalat =  ("0809", "0818", "0817", "0909","0908")
        query = "SELECT * from access where passwd =%s and user_name =%s"
        val = (login_password, login_username)
        cursor.execute(query, val)
        login_result = cursor.fetchone()
        print("""What Network would you like to purchase?
        1) Airtel
        2) GLO
        3) MTN
        4) 9Mobile""")
        answer = input(">>> ")
        if answer == "1":
            number = input(("Enter the phone number "))
            if number.isdigit() and len(number) == 11 and number.startswith(Airtel):
                amount = int(input("Enter the amount you want to purchase "))
                balance = login_result[8]
                if balance < amount:
                    print("You do not have sufficient balance to make this purchase")
                    print("Input 1 to go to the main menu and 2 to log out")
                    response = input(">>> ")
                    while True:
                        if response == "1":
                            mainMenu()
                            break
                        elif response == "2":
                            welcome()
                            break
                        else:
                            response = input("Invalid Input. Try again >>> ")
                else:
                    new_amount = balance - amount
                    val2 = (new_amount, login_result[0])
                    myquery = "UPDATE access SET account_balance =%s where id =%s"
                    cursor.execute(myquery, val2)
                    myconn.commit()
                    print("Please wait")
                    time.sleep(2)
                    print(f"You have successfully purchased {amount} airtime")
                    print("Input 1 to go to the main menu and 2 to log out")
                    response = input(">>> ")
                    while True:
                        if response == "1":
                            mainMenu()
                            break
                        elif response == "2":
                            welcome()
                            break
                        else:
                            response = input("Invalid Input. Try again >>> ")
            else:
                print("Enter a Valid Airtel number")
                time.sleep(1)
                buyAirtime()
        elif answer == "2":
            number = input(("Enter the phone number "))
            if number.isdigit() and len(number) == 11 and number.startswith(GLO):
                amount = int(input("Enter the amount you want to purchase "))
                balance = login_result[8]
                if balance < amount:
                    print("You do not have sufficient balance to make this purchase")
                    print("Input 1 to go to the main menu and 2 to log out")
                    response = input(">>> ")
                    while True:
                        if response == "1":
                            mainMenu()
                            break
                        elif response == "2":
                            welcome()
                            break
                        else:
                            response = input("Invalid Input. Try again >>> ")
                else:
                    new_amount = balance - amount
                    val2 = (new_amount, login_result[0])
                    myquery = "UPDATE access SET account_balance =%s where id =%s"
                    cursor.execute(myquery, val2)
                    myconn.commit()
                    print("Please wait")
                    time.sleep(2)
                    print(f"You have successfully purchased {amount} airtime")
                    print("Input 1 to go to the main menu and 2 to log out")
                    response = input(">>> ")
                    while True:
                        if response == "1":
                            mainMenu()
                            break
                        elif response == "2":
                            welcome()
                            break
                        else:
                            response = input("Invalid Input. Try again >>> ")
            else:
                print("Enter a Valid GLO number")
                time.sleep(1)
                buyAirtime()
        elif answer == "3":
            number = input(("Enter the phone number "))
            if number.isdigit() and len(number) == 11 and number.startswith(MTN):
                amount = int(input("Enter the amount you want to purchase "))
                balance = login_result[8]
                if balance < amount:
                    print("You do not have sufficient balance to make this purchase")
                    print("Input 1 to go to the main menu and 2 to log out")
                    response = input(">>> ")
                    while True:
                        if response == "1":
                            mainMenu()
                            break
                        elif response == "2":
                            welcome()
                            break
                        else:
                            response = input("Invalid Input. Try again >>> ")
                else:
                    new_amount = balance - amount
                    val2 = (new_amount, login_result[0])
                    myquery = "UPDATE access SET account_balance =%s where id =%s"
                    cursor.execute(myquery, val2)
                    myconn.commit()
                    print("Please wait")
                    time.sleep(2)
                    print(f"You have successfully purchased {amount} airtime")
                    print("Input 1 to go to the main menu and 2 to log out")
                    response = input(">>> ")
                    while True:
                        if response == "1":
                            mainMenu()
                            break
                        elif response == "2":
                            welcome()
                            break
                        else:
                            response = input("Invalid Input. Try again >>> ")
            else:
                print("Enter a Valid MTN number")
                time.sleep(1)
                buyAirtime()
        elif answer == "4":
            number = input(("Enter the phone number "))
            if number.isdigit() and len(number) == 11 and number.startswith(Etisalat):
                amount = int(input("Enter the amount you want to purchase "))
                balance = login_result[8]
                if balance < amount:
                    print("You do not have sufficient balance to make this purchase")
                    print("Input 1 to go to the main menu and 2 to log out")
                    response = input(">>> ")
                    while True:
                        if response == "1":
                            mainMenu()
                            break
                        elif response == "2":
                            welcome()
                            break
                        else:
                            response = input("Invalid Input. Try again >>> ")
                else:
                    new_amount = balance - amount
                    val2 = (new_amount, login_result[0])
                    myquery = "UPDATE access SET account_balance =%s where id =%s"
                    cursor.execute(myquery, val2)
                    myconn.commit()
                    print("Please wait")
                    time.sleep(2)
                    print(f"You have successfully purchased {amount} airtime")
                    print("Input 1 to go to the main menu and 2 to log out")
                    response = input(">>> ")
                    while True:
                        if response == "1":
                            mainMenu()
                            break
                        elif response == "2":
                            welcome()
                            break
                        else:
                            response = input("Invalid Input. Try again >>> ")
            else:
                print("Enter a Valid Etisalat number")
                time.sleep(1)
                buyAirtime()
        else:
            answer = input("Invalid input. Try again >>> ")
            buyAirtime()
    except ValueError:
        print("Amount must be in digits")
        buyAirtime()


# def deposit():
#     try:
#         query = "SELECT * from access where passwd =%s and user_name =%s"
#         val = (login_password, login_username)
#         cursor.execute(query, val)
#         login_result = cursor.fetchone()
#         amount = int(input(("Enter the amount you want to deposit ")))
#         new_amount = login_result[8] + amount
#         val2 = (new_amount, login_result[0])
#         myquery = "UPDATE access SET account_balance =%s where id =%s"
#         cursor.execute(myquery, val2)
#         myconn.commit()
#         print("Please wait")
#         time.sleep(2)
#         print(f"You have successfully deposited {amount} naira")
#         print("Input 1 to go to the main menu and 2 to log out")
#         response = input(">>> ")
#         while True:
#             if response == "1":
#                 mainMenu()
#                 break
#             elif response == "2":
#                 welcome()
#                 break
#             else:
#                 response = input("Invalid Input. Try again >>> ")
#     except ValueError:
#         print("Amount must be in digits")
#         deposit()


def adminOperation():
    try:
        global result2
        admin_password = "maranatha"
        admin = input("Enter admin's password ")
        if admin == admin_password:
            account_numb = int(input("Enter the customer account number "))
            query = "SELECT * from access where account_number =%s"
            val = (account_numb, )
            cursor.execute(query, val)
            result2 = cursor.fetchone()
            if result2 == None:
                print("Account number does not exist. Start again")
                adminOperation()
            else:
                deposit()
        else:
            print("Invalid Password")
            print("Input 1 to go to back")
            response = input(">>> ")
            while True:
                if response == "1":
                    welcome()
                    break
                else:
                    response = input("Invalid Input. Try again >>> ")
    except ValueError:
        print("Invalid Account number. Start again")
        adminOperation()


def deposit():
    try:
        amount = int(input(("Enter the amount you want to deposit ")))
        new_amount = result2[8] + amount
        val2 = (new_amount, result2[0])
        myquery = "UPDATE access SET account_balance =%s where id =%s"
        cursor.execute(myquery, val2)
        myconn.commit()
        print("Please wait")
        time.sleep(2)
        print(f"You have successfully deposited {amount} naira to {result2[1]} {result2[2]}")
        print("Input 1 to go to back")
        response = input(">>> ")
        while True:
            if response == "1":
                welcome()
                break
            else:
                response = input("Invalid Input. Try again >>> ")
    except ValueError:
        print("Amount must be in digits")
        deposit()

def cables():
    query = "SELECT * from access where passwd =%s and user_name =%s"
    val = (login_password, login_username)
    cursor.execute(query, val)
    login_result = cursor.fetchone()
    print("""Choose the decoder you want to use.
    1) Gotv
    2) Dstv
    3) Startimes
    """)
    decoder = input(">>> ")
    if decoder == "1" or decoder == "2" or decoder == "3":
        print("""Choose the subscription you want
        1) Basic
        2) Regular
        3) Compact
        4) Premium""")
        subscription = input(">>> ")
        if subscription == "1":
            print("This plan costs #5000 and lasts for 30 days. Do you still wish to continue?")
            response = input("Enter 'y' to continue and any other key to go back home ").lower()
            if response == "y":
                basic = 5000
                if login_result[8] < basic:
                    print("You currently do not have sufficient amount to purchase this subscription")
                    print("Input 1 to go to the main menu and 2 to log out")
                    response = input(">>> ")
                    while True:
                        if response == "1":
                            mainMenu()
                            break
                        elif response == "2":
                            welcome()
                            break
                        else:
                            response = input("Invalid Input. Try again >>> ")
                else:
                    new_amount = login_result[8] - basic
                    val2 = (new_amount, login_result[0])
                    myquery = "UPDATE access SET account_balance =%s where id =%s"
                    cursor.execute(myquery, val2)
                    myconn.commit()
                    print("Please wait")
                    time.sleep(2)
                    print(f"You have successfully purchased a basic plan")
                    print("Input 1 to go to the main menu and 2 to log out")
                    response = input(">>> ")
                    while True:
                        if response == "1":
                            mainMenu()
                            break
                        elif response == "2":
                            welcome()
                            break
                        else:
                            response = input("Invalid Input. Try again >>> ")
            else:
                mainMenu()
        elif subscription == "2":
            print("This plan costs #7500 and lasts for 30 days. Do you still wish to continue?")
            response = input("Enter 'y' to continue and any other key to go back home ").lower()
            if response == "y":
                regular = 7500
                if login_result[8] < regular:
                    print("You currently do not have sufficient amount to purchase this subscription")
                    print("Input 1 to go to the main menu and 2 to log out")
                    response = input(">>> ")
                    while True:
                        if response == "1":
                            mainMenu()
                            break
                        elif response == "2":
                            welcome()
                            break
                        else:
                            response = input("Invalid Input. Try again >>> ")
                else:
                    new_amount = login_result[8] - regular
                    val2 = (new_amount, login_result[0])
                    myquery = "UPDATE access SET account_balance =%s where id =%s"
                    cursor.execute(myquery, val2)
                    myconn.commit()
                    print("Please wait")
                    time.sleep(2)
                    print(f"You have successfully purchased a regular plan")
                    print("Input 1 to go to the main menu and 2 to log out")
                    response = input(">>> ")
                    while True:
                        if response == "1":
                            mainMenu()
                            break
                        elif response == "2":
                            welcome()
                            break
                        else:
                            response = input("Invalid Input. Try again >>> ")
            else:
                mainMenu()
        elif subscription == "3":
            print("This plan costs #10500 and lasts for 30 days. Do you still wish to continue?")
            response = input("Enter 'y' to continue and any other key to go back home ").lower()
            if response == "y":
                compact = 10500
                if login_result[8] < compact:
                    print("You currently do not have sufficient amount to purchase this subscription")
                    print("Input 1 to go to the main menu and 2 to log out")
                    response = input(">>> ")
                    while True:
                        if response == "1":
                            mainMenu()
                            break
                        elif response == "2":
                            welcome()
                            break
                        else:
                            response = input("Invalid Input. Try again >>> ")
                else:
                    new_amount = login_result[8] - compact
                    val2 = (new_amount, login_result[0])
                    myquery = "UPDATE access SET account_balance =%s where id =%s"
                    cursor.execute(myquery, val2)
                    myconn.commit()
                    print("Please wait")
                    time.sleep(2)
                    print(f"You have successfully purchased a compact plan")
                    print("Input 1 to go to the main menu and 2 to log out")
                    response = input(">>> ")
                    while True:
                        if response == "1":
                            mainMenu()
                            break
                        elif response == "2":
                            welcome()
                            break
                        else:
                            response = input("Invalid Input. Try again >>> ")
            else:
                mainMenu()
        elif subscription == "4":
            print("This plan costs #13000 and lasts for 30 days. Do you still wish to continue?")
            response = input("Enter 'y' to continue and any other key to go back home ").lower()
            if response == "y":
                premium = 13000
                if login_result[8] < premium:
                    print("You currently do not have sufficient amount to purchase this subscription")
                    print("Input 1 to go to the main menu and 2 to log out")
                    response = input(">>> ")
                    while True:
                        if response == "1":
                            mainMenu()
                            break
                        elif response == "2":
                            welcome()
                            break
                        else:
                            response = input("Invalid Input. Try again >>> ")
                else:
                    new_amount = login_result[8] - premium
                    val2 = (new_amount, login_result[0])
                    myquery = "UPDATE access SET account_balance =%s where id =%s"
                    cursor.execute(myquery, val2)
                    myconn.commit()
                    print("Please wait")
                    time.sleep(2)
                    print(f"You have successfully purchased a premium plan")
                    print("Input 1 to go to the main menu and 2 to log out")
                    response = input(">>> ")
                    while True:
                        if response == "1":
                            mainMenu()
                            break
                        elif response == "2":
                            welcome()
                            break
                        else:
                            response = input("Invalid Input. Try again >>> ")
            else:
                mainMenu()
        else:
            print("Invalid input. Try again.")
            cables()
    else:
        print("Invalid input. Try again.")
        cables()


def reset():
    password = input("Enter your new password ")
    if not password.isdigit() or len(password) <= 3:
        print("Password must be 4 or more digits")
        reset()
    else:
        confirm_password = input("Confirm your new password ")
        if password == confirm_password:
            query = "SELECT * from access where passwd =%s and user_name =%s"
            val = (login_password, login_username)
            cursor.execute(query, val)
            login_result = cursor.fetchone()
            val2 = (password, login_result[0])
            myquery = "UPDATE access SET passwd =%s where id =%s"
            cursor.execute(myquery, val2)
            myconn.commit()
            val3 = (confirm_password, login_result[0])
            myquery2 = "UPDATE access SET confirmpasswd =%s where id =%s"
            cursor.execute(myquery2, val3)
            myconn.commit()
            print("Please wait")
            time.sleep(2)
            print("Password successfully reset")
            print("Input 1 to log in and 2 to go home")
            response = input(">>> ")
            while True:
                if response == "1":
                    login()
                    break
                elif response == "2":
                    welcome()
                    break
                else:
                    response = input("Invalid Input. Try again >>> ")
        else:
            print("Password does not match. Try again")
            reset()
            