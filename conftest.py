import boto3
import time
import pytest

region = "ap-south-1"
key_id = ""
secret_id = ""


@pytest.fixture
def setup():
    client = boto3.client('s3',
                          region_name=region,
                          aws_access_key_id=key_id,
                          aws_secret_access_key=secret_id
                          )
    response = client.create_bucket(
        ACL='public-read',
        Bucket='kanchi-aws',
        CreateBucketConfiguration={
            'LocationConstraint': 'ap-south-1'
        }
    )
    time.sleep(30)
    ec2 = boto3.client('ec2',
                       region_name=region,
                       aws_access_key_id=key_id,
                       aws_secret_access_key=secret_id
                       )
    securitygroup = ec2.create_security_group(GroupName='open-all', Description='all traffic',
                                              VpcId='vpc-03db1468')
    sg_id = securitygroup['GroupId']
    ec2.authorize_security_group_ingress(
        GroupId=sg_id,
        IpPermissions=[
            {'IpProtocol': '-1',
             'FromPort': 0,
             'ToPort': 65535,
             'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}
        ])

    yield
    re = client.delete_bucket(Bucket='kanchi-aws')
    ec2.delete_security_group(
        GroupId=sg_id

    )
