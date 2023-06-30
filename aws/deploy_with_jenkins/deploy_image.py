import boto3
import os
import time
import paramiko
import sys
import requests
import base64

app_name = os.getenv("APP")
image = os.getenv("IMAGE")
region = os.getenv("REGION")
workspace_path = os.getenv("WORKSPACE")

print(f"Starting deployment of {app_name} app in {region} with {image} image")

client = boto3.client('ec2', region_name=region)

print(f"Check for healthy instances")
# make list of instances, that passed both status checks
healthy_instances_id = []
instance_statuses = client.describe_instance_status()
for instance_status in instance_statuses["InstanceStatuses"]:
    if instance_status["InstanceStatus"]["Status"] == "ok" and instance_status["SystemStatus"]["Status"] == "ok":
        healthy_instances_id.append(instance_status["InstanceId"])

if len(healthy_instances_id) == 0:
    print("Sorry, there is no healthy instances at the moment")
    sys.exit(1)

print(f"Making list of healthy instances IPs with tag 'Name: {app_name}'")
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

print(f"Starting deployment")
# login at each server and do docker login, run container, make sure it's in running status and do simple HTTP healthcheck to make sure app is available
for ip in instances_public_ip:
    print(f"Logging into server {ip}")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    user_home_dir = os.getenv("HOME")
    ssh.connect(hostname=ip, username="ubuntu", key_filename=user_home_dir + "/.ssh/id_rsa")
    ecr = boto3.client('ecr', region_name=region)
    repo_uri = os.getenv("REPO_URI")
    # get ECR token, decode and format it
    token = ecr.get_authorization_token()['authorizationData'][0]['authorizationToken']
    ecr_username, ecr_password = base64.b64decode(token).decode('utf-8').split(":")
    # make list of running containers and kill them
    running_containers_in, running_containers_out, running_containers_err = ssh.exec_command('sudo docker ps -q')
    running_containers = running_containers_out.readlines()
    for container in running_containers:
        print(container)
        container_in, container_out, container_err = ssh.exec_command(f'sudo docker kill {container}')
    
    # cleanup Docker, login to ECR witj token and run container
    stdin, stdout, stderr = ssh.exec_command(f'sudo docker system prune -af && echo {ecr_password} | sudo docker login -u {ecr_username} --password-stdin {repo_uri} && sudo docker run -d --name {app_name} -p 8080:80 {image}')

    # print out command output and error, if any
    while True:
        print(stdout.read().decode(), end='')
        if stdout.channel.exit_status_ready():
            break

    while True:
        print(stderr.read().decode(), end='')
        if stderr.channel.exit_status_ready():
            break

    # health check
    status_checks = 1
    while True:
        time.sleep(5)
        print(f"Status check #{status_checks}")
        stdin, stdout, stderr = ssh.exec_command(f'sudo docker ps --filter status=running')
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
