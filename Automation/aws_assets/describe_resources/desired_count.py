import boto3

def count(logger,credentials,account,account_name):
    logger.info(f"{account_name} >> Start Describing ASG & ECS SVC Desired Count...")

    output = []

    region_list = [
        # "us-east-1",
        # "us-east-2",
        # "us-west-1",
        # "us-west-2",
        # "ap-south-1",
        # "ap-northeast-3",
        # "ap-northeast-2",
        # "ap-southeast-1",
        # "ap-southeast-2",
        "ap-northeast-1"
        # "ca-central-1",
        # "eu-central-1",
        # "eu-west-1",
        # "eu-west-2",
        # "eu-west-3",
        # "eu-north-1",
        # "sa-east-1"
    ]

    for region in region_list:
        logger.info(f"get in Region - {region} ...")
        try:
        
            asg_client = boto3.client(
                'autoscaling',
                aws_access_key_id=credentials['AccessKeyId'],
                aws_secret_access_key=credentials['SecretAccessKey'],
                aws_session_token=credentials['SessionToken'],
                region_name = region
            )

            ecs_client = boto3.client(
                'ecs',
                aws_access_key_id=credentials['AccessKeyId'],
                aws_secret_access_key=credentials['SecretAccessKey'],
                aws_session_token=credentials['SessionToken'],
                region_name = region
            )

            asg_response = ''
            asg_next_token = ''
            first_check = True

            while asg_next_token is not None:
                
                if first_check:
                    asg_response = asg_client.describe_auto_scaling_groups()
                    first_check = False
                else:
                    asg_response = asg_client.describe_auto_scaling_groups(NextToken=asg_next_token)
                for asg in asg_response['AutoScalingGroups']:
                    asg_name = asg['AutoScalingGroupName']
                    asg_desired_count = asg['DesiredCapacity']
                    asg_min_count = asg['MinSize']
                    asg_max_count = asg['MaxSize']
                    try:
                        svc_response = ecs_client.list_services(cluster=asg_name)
                        service_arns = svc_response['serviceArns']
                        service_len = len(service_arns)
                        for e in range(service_len):
                            service_arn = service_arns[e]
                            #service_arn = 'arn:aws:ecs:ap-northeast-1:899117875930:service/onstove-sandbox-i-batch'
                            count_response = ''
                            count_next_token = ''
                            count_first_check = True
                            while count_next_token is not None:
                                if count_first_check:
                                    count_response = ecs_client.describe_services(
                                        cluster=asg_name,
                                        services=[service_arn]
                                    )
                                    count_first_check = False
                                else:
                                    count_response = ecs_client.describe_services(
                                        cluster=asg_name,
                                        services=[service_arn],
                                        NextToken=count_next_token
                                    )
                                for service in count_response['services']:
                                    svc_name = service['serviceName']
                                    svc_desired_count = service['desiredCount']
                                    svc_running_count = service['runningCount']
                                    svc_pending_count = service['pendingCount']
                                    if svc_name == asg_name:
                                        output.append({
                                            "ACCOUNT" : f"'{account}",
                                            "ACCOUNT_NAME" : account_name,
                                            "REGION" : region,
                                            "ASG_NAME" : asg_name,
                                            "ASG_DESIRED_COUNT" : asg_desired_count,
                                            "ASG_MIN_COUNT" : asg_min_count,
                                            "ASG_MAX_COUNT" : asg_max_count,
                                            "SVC_NAME" : svc_name,
                                            "SVC_DESIRED_COUNT" : svc_desired_count,
                                            "SVC_RUNNING_COUNT" : svc_running_count,
                                            "SVC_PENDING_COUNT" : svc_pending_count
                                        })
                                        logger.info("ASG and ECS SVC Info are appended.")
                                if 'NextToken' in count_response:
                                    count_next_token = count_response['NextToken']
                                else:
                                    count_next_token = None
                        # if 'NextToken' in svc_response:
                        #     svc_next_token = svc_response['NextToken']
                        # else:
                        #     svc_next_token = None
                    except Exception as e:
                            continue
                            # logger.info("Error!!")
                            # logger.exception("message")
                if 'NextToken' in asg_response:
                    asg_next_token = asg_response['NextToken']
                else:
                    asg_next_token = None
        except Exception as e:
            logger.info("Error!!")
            logger.exception("message")
    
    logger.info(f"{account_name} >> Finish Describing ASG & ECS SVC Desired Count!")
    return output