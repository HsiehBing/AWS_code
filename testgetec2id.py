import boto3
region = 'ap-northeast-1'
ec2_client = boto3.client('ec2', region_name=region)

instances = ec2_client.describe_instances()
ID_list= []

for instance in instances['Reservations']:
    instanceID = instance['Instances'][0]['InstanceId']
    ID_list.append(instanceID)

print(ID_list)
