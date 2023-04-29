my_list = [1, 2, 2, 4, 4, 5, 6, 8, 10, 13, 22, 35, 52, 83]

new_list = []

user_input = input("Please, provide number and I'll return a list that contains only those elements from my_list that are higher than the number\n")

for item in my_list:
    if item > int(user_input):
        new_list.append(item)

print(new_list)