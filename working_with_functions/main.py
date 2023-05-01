from helper import name_and_age, letter_calc, even_numbers

# print out the name and age of the youngest employee
employees = [{ "name": "Tina", "age": 30, "birthday": "1990-03-10", "job": "DevOps Engineer", "address": { "city": "New York", "country": "USA" } }, { "name": "Tim", "age": 35, "birthday": "1985-02-21", "job": "Developer", "address": { "city": "Sydney", "country": "Australia" } }]

employees_name_and_age = name_and_age(employees)
print(employees_name_and_age)

# calculates the number of upper case letters and lower case letters
string_letter_calc = letter_calc("This Is My String")
print(string_letter_calc)

# print even numbers from a provided list
list_of_numbers = [10, 22, 34, 102, 122, 1023, 2222]

even_list_of_numbers = even_numbers(list_of_numbers)
print(f"Even numbers are: {even_list_of_numbers}")