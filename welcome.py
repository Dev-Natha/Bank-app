import time
print("""
Welcome to Natha Banking Institute. Which of the following banks would you like to use?""")
time.sleep(1)
print("""
1) Access
2) Polaris
3) Zenith
""")
answer = input(">>> ")
if answer == "1":
    from access import welcome
    welcome()
elif answer == "2":
    from polaris import welcome
    welcome()
elif answer == "3":
    from zenith import welcome
    welcome()
else:
    print("Invalid input")