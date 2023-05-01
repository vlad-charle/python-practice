employees = [{ "name": "Tina", "age": 30, "birthday": "1990-03-10", "job": "DevOps Engineer", "address": { "city": "New York", "country": "USA" } }, { "name": "Tim", "age": 35, "birthday": "1985-02-21", "job": "Developer", "address": { "city": "Sydney", "country": "Australia" } }]

# print name, job and city for all employees
requested_data = ["name", "job", "city"]
for employee in employees:
    for data in requested_data:
        if data == "city" or data == "country":
            print(f"employee {data} is: {employee['address'][data]}")
        else:
            print(f"employee {data} is: {employee[data]}")

# print country of the second employee in the list by accessing it directly without the loop
print(employees[1]['address']['country'])