import boto3
import requests
import schedule
import paramiko
import os

healthcheck_count = 1
healthcheck_fails = 0

user_home_dir = os.getenv("HOME")

def healthcheck():

    global healthcheck_count
    print(f"Running healthcheck #{healthcheck_count}")
    healthcheck_count += 1
    
    client = boto3.client('ec2')

    # make list of instances, that passed both status checks
    healthy_instances_id = []
    instance_statuses = client.describe_instance_status()
    for instance_status in instance_statuses["InstanceStatuses"]:
        if instance_status["InstanceStatus"]["Status"] == "ok" and instance_status["SystemStatus"]["Status"] == "ok":
            healthy_instances_id.append(instance_status["InstanceId"])

    if len(healthy_instances_id) == 0:
        print("Sorry, there is no healthy instances at the moment")
        return

    # make list of public IPs of instances, that in running state
    instances_public_ip = []
    instance_reservations = client.describe_instances(InstanceIds=healthy_instances_id)
    for r in instance_reservations["Reservations"]:
        instances = r["Instances"]
        for instance in instances:
            if instance["State"]["Name"] == "running":
                instances_public_ip.append(instance["PublicIpAddress"])

    # make HTTP request to each healthy instance public IP,
    # if there is an error, count it and when there is 5 consequence errors initiate self-recovery 
    # by logging into server and restarting container
    for ip in instances_public_ip:
        global healthcheck_fails
        try:
            response = requests.get(f"http://{ip}:8080")

            try:
                response.raise_for_status()
            except requests.exceptions.HTTPError as error:
                print("HTTP status is not 200, error: " + str(error))
                healthcheck_fails += 1
                print(f"Number of consequently failed healthchecks is {healthcheck_fails}")
                if healthcheck_fails == 5:
                    self_recovery(ip)

            print(f"IP {ip} is healthy")
            healthcheck_fails = 0
        except requests.exceptions.ConnectionError as error:
            print(f"Cannot establish connection for IP: {ip}, error: " + str(error))
            healthcheck_fails += 1
            print(f"Number of consequently failed healthchecks is {healthcheck_fails}")
            if healthcheck_fails == 5:
                self_recovery(ip)

def self_recovery(ip):
    global user_home_dir
    print("Starting self-recovery")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=ip, username="ubuntu", key_filename=user_home_dir + "/.ssh/id_rsa")
    print(f"Logged into server {ip}")
    stdin, stdout, stderr = ssh.exec_command('sudo docker ps -a')
    print(stdout.readlines())
    containers = stdout.readlines()
    container_id = containers[1].split(" ")[0]
    print(f"Got container ID: {container_id}")
    stdin, stdout, stderr = ssh.exec_command(f'sudo docker restart {container_id}')
    cmd_output = stdout.readlines()
    if container_id in cmd_output[0]:
        print(f"Sucessfully restarted container ID: {container_id}")

schedule.every(10).seconds.do(healthcheck)

while True:
    schedule.run_pending()