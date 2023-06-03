import boto3

client = boto3.client('iam')

response = client.list_users()
users = response["Users"]

user_created_date = []
for user in users:
    print(f"User {user['UserName']} was created at {user['CreateDate']}")
    user_created = {"UserName": user['UserName'], "UserId": user['UserId'], "CreateDate": user['CreateDate']}
    user_created_date.append(user_created)

# get user created most recently, max in list of dictionaries by key in the dict
most_recently_created_user = max(user_created_date, key=lambda d: d["CreateDate"])

print(f"{most_recently_created_user['UserName']} user is the latest one created, creation date is {most_recently_created_user['CreateDate']}")