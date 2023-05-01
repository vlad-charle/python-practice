from random import randint

user_input = ''
random_number = randint(0,10)
tries = 0

while True:

    user_input = input("Hey! Guess a number from 0 to 10!\n")

    try:
        user_try = int(user_input)
    except ValueError:
        print(f"Hey! {user_input} is not a number!")
        continue

    if user_try > 10:
        print(f"Hey! {user_try} is higher then 10, please, make correct input!")
    elif user_try == random_number:
        tries += 1
        break
    else:
        print(f"Oh, sorry, but {user_try} is wrong number, please, try again!")
        tries += 1
        continue

print(f"Wow! Congrats! {user_try} is correct! You beat it in {tries} tries, well done!")