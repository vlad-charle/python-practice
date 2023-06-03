import boto3

client = boto3.client('ec2')

response = client.describe_subnets()
subnets = response["Subnets"]

for subnet in subnets:
    print(subnet["SubnetId"])