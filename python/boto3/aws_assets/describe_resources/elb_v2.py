import boto3

def elb_v2(logger,credentials,account,account_name):
    logger.info(f"{account_name} >> Start Describing ELB2...")
    output = []
    client = boto3.client(
        'elbv2',
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

            for elb in elb_response['LoadBalancers']:
                elb_name = elb['LoadBalancerName']
                elb_dns = elb['DNSName']
                elb_arn = elb['LoadBalancerArn']
                
                target_response = client.describe_target_groups(
                    LoadBalancerArn=elb_arn
                )
                for target in target_response['TargetGroups']:
                    target_arn = target['TargetGroupArn']

                    instance_response = client.describe_target_health(
                        TargetGroupArn=target_arn
                    )
                    for instance in instance_response['TargetHealthDescriptions']:
                        instance_id = instance['Target']['Id']
                        instance_state = instance['TargetHealth']['State'] 
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
    logger.info(f"{account_name} >> Finish Describing ELB2...")
    return output