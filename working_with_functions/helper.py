def name_and_age(list_of_dict):
    
    name_age_dict = {}
    for employee in list_of_dict:
        name_age_dict[employee['name']] = employee['age']
    
    min_value = min(name_age_dict.values())
    min_value_key = min(name_age_dict, key=name_age_dict.get)
    return f"The youngest employees is {min_value_key}, the age is {min_value}"

def letter_calc(string):

    count_lowercase = 0
    count_uppercase = 0
    for letter in string:
        if letter.isupper() == True:
            count_uppercase += 1
        elif letter.islower() == True:
            count_lowercase += 1
        else:
            continue
    
    return f"There is {count_uppercase} uppercase letter and {count_lowercase} lowercase letters in string:'{string}'"

def even_numbers(list):

    even_numbers_list = []
    for number in list:
        if number % 2 == 0:
            even_numbers_list.append(number)
    
    return even_numbers_list

