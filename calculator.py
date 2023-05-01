user_input = ''
user_input_count = 0

while user_input != 'exit':

    user_input = input("Please, provide 2 numbers and action (plus, minus, multiply, divide) separated by colon, i.e. 2:10:divide\n")
    user_input_list = user_input.split(":")
    
    try:
        number_1 = int(user_input_list[0])
        number_2 = int(user_input_list[1])
    except ValueError:
        print(f"This is not numbers, your input is invalid, correct format is number:number:action")
        user_input_count += 1
        continue
    
    try:
        action = user_input_list[2]
    except IndexError:
        print(f"You messed up with formatting, it should be number:number:action")
        user_input_count += 1
        continue

    actions = ["plus", "minus", "multiply", "divide"]
    if action not in actions:
        print(f"{action} is not correct action, it should plus, minus, multiply or divide")
        user_input_count += 1
        continue
    elif action == "plus":
        result = number_1 + number_2
    elif action == "minus":
        result = number_1 - number_2
    elif action == "multiply":
        result = number_1 * number_2
    elif action == "divide":
        try:
            result = number_1 / number_2
        except ZeroDivisionError:
            print(f"You cannot divide by zero!")
            user_input_count += 1
            continue
    
    print(f"Result for {number_1} {action} {number_2} is {result}")
    user_input_count += 1

print(f"Thank you for using this program, you did {user_input_count} times!")