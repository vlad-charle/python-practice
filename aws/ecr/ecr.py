import boto3

ecr = boto3.client('ecr-public')

repos = ecr.describe_repositories()['repositories']

for repo in repos:
    print(f"ECR repository name is: {repo['repositoryName']}")
    images = ecr.describe_images(
    repositoryName=repo['repositoryName']
    )['imageDetails']
    if images == []: # if repo is empty, print message and skip remaining logic
        print(f"Sorry, but {repo['repositoryName']} repo is empty")
        continue
    for image in images:
        if len(image['imageTags']) == 1: # list with 1 element breaks sorted(), so we avoid it with additional check
            print(f"Image with digest {image['imageDigest']} has only 1 tag: {image['imageTags'][0]}")
        else:
            sorted_tags = sorted(image['imageTags'], reverse=True)
            print(f"Image with digest {image['imageDigest']} tags are:") # image names are the same within repo, so we use digest to distinguish them
            for tag in sorted_tags:
                print(tag)