import boto3
import requests
import schedule

healthcheck_count = 1

def healthcheck ():

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

    # make HTTP request to each healthy instance public IP 
    for ip in instances_public_ip:

        try:
            response = requests.get(f"http://{ip}:8080")

            try:
                response.raise_for_status()
            except requests.exceptions.HTTPError as error:
                print("HTTP status is not 200, error: " + str(error))

            print(f"IP {ip} is healthy")
        except requests.exceptions.ConnectionError as error:
            print(f"Cannot establish connection for IP: {ip}, error: " + str(error))


schedule.every(10).seconds.do(healthcheck)

while True:
    schedule.run_pending()