import boto3
import os

app_name = os.getenv("APP")
region = os.getenv("REGION")

ecr = boto3.client('ecr', region_name=region)

repos = ecr.describe_repositories()['repositories']
for repo in repos:
    repo_uri = repo['repositoryUri']
    if app_name in repo_uri:
        app_repo_uri = repo_uri

print(app_repo_uri)