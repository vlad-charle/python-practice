import datetime

user_bd = input("Please, provide your birthday in format dd.mm.yyyy:\n")

user_bd_split = user_bd.split(".")

if len(user_bd_split) < 3:
    print(f"Hey! You have provided your BD in a wrong format, I expect dd.mm.yyyy, but you have provided {user_bd}")
    exit()

for index, element in enumerate(user_bd_split):
    try:
        user_bd_element = int(user_bd_split[index])
    except ValueError:
        print(f"Hey! You have provided your BD in a wrong format, I expect dd.mm.yyyy, but you have provided {user_bd}")
        exit()
    if index == 0:
        user_bd_day = int(user_bd_split[index])
    elif index == 1:
        user_bd_month = int(user_bd_split[index])
    elif index == 2:
        user_bd_year = int(user_bd_split[index])
    else:
        print(f"Hey! You have provided your BD in a wrong format, I expect dd.mm.yyyy, but you have provided {user_bd}")
        exit()

curr_date = datetime.datetime.now()
curr_year = int(datetime.datetime.strftime(curr_date, "%Y"))

if user_bd_day > 31:
    print(f"Hey! It cannot be more then 31 days in a month!")
    exit()
if user_bd_month > 12:
    print(f"Hey! It cannot be more then 12 months in a year!")
    exit()
if user_bd_year > curr_year:
    print(f"Hey! You cannot be born in future!")
    exit()
if user_bd_month == 2 and user_bd_day > 28:
    print(f"Hey! There is 28 days max in February!")
    exit()

next_bd = datetime.datetime(curr_year, user_bd_month, user_bd_day)

next_bd_delta = next_bd - curr_date

print(f"It's {next_bd_delta.days} days till your birthday!")
