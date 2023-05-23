import boto3

def maintenance(logger,credentials,account,account_name):
    logger.info(f"{account_name} >> Start Describing maintenance...")

    output = []

    health_client = boto3.client(
        'health',
        aws_access_key_id=credentials['AccessKeyId'],
        aws_secret_access_key=credentials['SecretAccessKey'],
        aws_session_token=credentials['SessionToken'],
        region_name = "us-east-1"
    )
    
    event_response = ''
    next_token = ''
    first_check = True
    
    while next_token is not None:
        if first_check:
            event_response = health_client.describe_events(
                filter={
                    'eventTypeCategories': ['scheduledChange'],
                    'eventStatusCodes': ['open','upcoming']
                }
            )
            first_check = False
        else:
            event_response = health_client.describe_events(
                filter={
                    'eventTypeCategories': ['scheduledChange'],
                    'eventStatusCodes': ['open','upcoming']
                },
                nextToken=next_token
            )
    
        for event in event_response["events"]:
            
            affected_entity = ''
            
            try:
                entity_response = health_client.describe_affected_entities(
                    filter={
                        'eventArns': [
                            event["arn"]
                        ]
                    }
                )
                
                affected_entity = entity_response["entities"][0]["entityValue"]
            except Exception as e:
                logger.info("Error!!")
                logger.exception("message")
                    
            
            host_name = ''
            private_ip = ''
            
            try:
                if event["service"] == 'EC2':
    
                    ec2_client = boto3.client(
                        'ec2',
                        aws_access_key_id=credentials['AccessKeyId'],
                        aws_secret_access_key=credentials['SecretAccessKey'],
                        aws_session_token=credentials['SessionToken'],
                        region_name=event["region"]
                    )
                    
                    instances_response = ec2_client.describe_instances(
                        InstanceIds=[
                            affected_entity
                        ]
                    )
                    
                    instance = instances_response['Reservations'][0]['Instances'][0]
                    if not "Tags" in instance:
                        host_name = ''
                    else:
                        for tag in instance['Tags']:
                            if tag['Key'] == 'Name':
                                host_name = tag['Value']
                                break
                
                    private_ip = instance["PrivateIpAddress"]
            except Exception as e:
                logger.info("Error!!")
                logger.exception("message")
            
            output.append({
                "ACCOUNT" : f"'{account}",
                "ACCOUNT_NAME" : account_name,
                "Service" : event["service"],
                "Event Type Category" : event["eventTypeCode"],
                "Region" : event["region"],
                "Start Time" : event["startTime"],
                "End Time" : event["endTime"],
                "Affected entities" : affected_entity,
                "Instance Name" : host_name,
                "Private IP" : private_ip
            })
        if 'nextToken' in event_response:
            next_token = event_response['nextToken']
        else:
            next_token = None
    
    logger.info(f"{account_name} >> Finish Describing maintenance...")
    return output