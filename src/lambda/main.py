import boto3
import json
import os

ZONE_ID = os.environ['HOSTED_ZONE_ID']
zone_domain = os.environ['HOSTED_ZONE_DOMAIN']

def get_instance_private_ip(instance_id, instance_state):

    ec2 = boto3.client('ec2')

    instance_data = ec2.describe_instances(
        InstanceIds=[instance_id],
    )

    private_ip = '0.0.0.0'
    if instance_state != 'terminated':
        private_ip = instance_data['Reservations'][0]['Instances'][0]['PrivateIpAddress']
    hostname = instance_data['Reservations'][0]['Instances'][0]['Tags'][0]['Value']

    return hostname, private_ip


def perform_route53_update(route53, action, hostname, private_ip):

    return route53.change_resource_record_sets(
            HostedZoneId=ZONE_ID,
            ChangeBatch={
                "Comment": "Updated by Lambda DDNS",
                "Changes": [
                    {
                        "Action": action,
                        "ResourceRecordSet": {
                            "Name": f"{hostname}.{zone_domain}",
                            "Type": 'A',
                            "TTL": 60,
                            "ResourceRecords": [
                                {
                                    "Value": private_ip
                                },
                            ]
                        }
                    },
                ]
            }
        )


def create_or_update_dns_record(hostname, private_ip):

    route53 = boto3.client('route53')

    response = perform_route53_update(route53, 'UPSERT', hostname, private_ip)
    
    return response


def delete_dns_record(hostname, private_ip):

    route53 = boto3.client('route53')

    response = route53.list_resource_record_sets(
        HostedZoneId=ZONE_ID,
        StartRecordName=f"{hostname}.{zone_domain}"
    )

    private_ip = response['ResourceRecordSets'][0]['ResourceRecords'][0]['Value']

    response = perform_route53_update(route53, 'DELETE', hostname, private_ip)
    
    return response


def lambda_handler(event, context):

    instance_id, instance_state = event['detail']['instance-id'], event['detail']['state']

    hostname, private_ip = get_instance_private_ip(instance_id, instance_state)

    if instance_state == 'terminated':
        print("launch cleanup", hostname, private_ip)
        output = delete_dns_record(hostname, private_ip)
        print(output)
    else:
        print("launch create/update", hostname, private_ip)
        output = create_or_update_dns_record(hostname, private_ip)
        print(output)

    return {
        'statusCode' : 200,
        'body': "Hello World"
    }
