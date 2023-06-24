import boto3
import os
import time
import paramiko
import sys
import requests

app_name = os.getenv("APP")
ssh_key = os.getenv("SSH_KEY")
image = os.getenv("IMAGE")
region = os.getenv("REGION")

client = boto3.client('ec2', region_name=region)

# make list of instances, that passed both status checks
healthy_instances_id = []
instance_statuses = client.describe_instance_status()
for instance_status in instance_statuses["InstanceStatuses"]:
    if instance_status["InstanceStatus"]["Status"] == "ok" and instance_status["SystemStatus"]["Status"] == "ok":
        healthy_instances_id.append(instance_status["InstanceId"])

if len(healthy_instances_id) == 0:
    print("Sorry, there is no healthy instances at the moment")
    sys.exit(1)

# make list of public IPs of instances, that in running state
instances_public_ip = []
instance_reservations = client.describe_instances(
    InstanceIds=healthy_instances_id, 
    Filters=[
        {
            'Name': 'tag:Name',
            'Values': [app_name]
        },
    ]
)
for r in instance_reservations["Reservations"]:
    instances = r["Instances"]
    for instance in instances:
        if instance["State"]["Name"] == "running":
            instances_public_ip.append(instance["PublicIpAddress"])

# login at each server and do docker login, run container, make sure it's in running status and do simple HTTP healthcheck to make sure app is available
for ip in instances_public_ip:
    print(f"Logging into server {ip}")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # create key object from env var value
    key = paramiko.RSAKey.from_private_key(paramiko.StringIO(ssh_key))
    ssh.connect(hostname=ip, username="ubuntu", pkey=key)
    ecr = boto3.client('ecr', region_name=region)
    token = ecr.get_authorization_token()['authorizationData'][0]['authorizationToken']
    stdin, stdout, stderr = ssh.exec_command(f'echo {token} | sudo docker login -u AWS --password-stdin && sudo docker run --name {app_name} -p 8080:80 {image}')
    print(stdout.readlines())
    status_checks = 1
    while True:
        time.sleep(5)
        print(f"Status check #{status_checks}")
        stdin, stdout, stderr = ssh.exec_command(f'docker ps --filter status=running')
        container_status = stdout.readlines()
        if container_status[1]:
            print(f"{app_name} container started succesfully")
            break
        else:
            print("Container is not yet in running state")
            status_checks += 1
            if status_checks == 6:
                print("Something went wrong, container cannot get to running state")
                sys.exit(1)
    try:
        response = requests.get(f"http://{ip}:8080")

        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as error:
            print("HTTP status is not 200, error: " + str(error))

        print(f"IP {ip} is healthy")
    except requests.exceptions.ConnectionError as error:
        print(f"Cannot establish connection for IP: {ip}, error: " + str(error))
