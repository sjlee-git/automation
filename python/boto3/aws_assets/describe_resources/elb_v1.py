import boto3

def elb_v1(logger,credentials,account,account_name):
    logger.info(f"{account_name} >> Start Describing ELB...")
    output = []
    client = boto3.client(
        'elb',
        aws_access_key_id=credentials['AccessKeyId'],
        aws_secret_access_key=credentials['SecretAccessKey'],
        aws_session_token=credentials['SessionToken'],
        region_name='ap-northeast-1'
    )
    try:
        elb_response = ''
        next_token = ''
        first_check = True

        while next_token is not None:
            
            if first_check:
                elb_response = client.describe_load_balancers()
                first_check = False
            else:
                elb_response = client.describe_load_balancers(Marker=next_token)

            for elb in elb_response['LoadBalancerDescriptions']:
                elb_name = elb['LoadBalancerName']
                elb_dns = elb['DNSName']
                
                instance_response = client.describe_instance_health(
                    LoadBalancerName=elb_name
                )
                for instance in instance_response['InstanceStates']:
                    instance_id = instance['InstanceId']
                    instance_state = instance['State'] 
                    output.append({
                        "ACCOUNT_NAME" : account_name,
                        "ELB_NAME" : elb_name,
                        "ELB_DNS" : elb_dns,
                        "Instance_ID" : instance_id,
                        "Instance State" : instance_state
                    })
            if 'NextMarker' in elb_response:
                next_token = elb_response['NextMarker']
            else:
                next_token = None
    except Exception as e:
                logger.info("Error!!")
                logger.exception("message")
    logger.info(f"{account_name} >> Finish Describing ELB...")
    return output