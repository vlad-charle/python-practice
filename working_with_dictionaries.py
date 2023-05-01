employee = { "name": "Tim", "age": 30, "birthday": "1990-03-10", "job": "DevOps Engineer" }

# update value for key
employee["job"] = "Software Engineer"

# delete kv
del employee["age"]

# print each kv
for key, value in employee.items():
    print("kv is: " + key, value)

dict_one = {'a': 100, 'b': 400} 
dict_two = {'x': 300, 'y': 200}

# merge 2 dictionaries
dict_three = dict_one | dict_two
print("new dictionary is:")
print(dict_three)

# sums up all values in dictionary
dict_sum = 0

for each in dict_three:
    dict_sum = dict_sum + dict_three[each]

print("sum of all values in the dictionary is: " + str(dict_sum))

# get max and min of the dict values
print("max value in the dictionary is: " + str(max(dict_three.values())))

print("min value in the dictionary is: " + str(min(dict_three.values())))