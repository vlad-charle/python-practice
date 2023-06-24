import boto3
import os

app_name = os.getenv("APP")
region = os.getenv("REGION")

ecr = boto3.client('ecr', region_name=region)

images = ecr.describe_images(
    repositoryName=app_name
    )
image_list = []
for image in images['imageDetails']:
    image_list.append(image['imageTags'][0])

sorted_list = sorted(image_list, reverse=True)

print(sorted_list)