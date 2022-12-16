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
        
            client = boto3.client(
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
            ecs_response = ''
            next_token = ''
            first_check = True

            while next_token is not None:
                
                if first_check:
                    asg_response = client.describe_auto_scaling_groups()
                    first_check = False
                else:
                    asg_response = client.describe_auto_scaling_groups(NextToken=next_token)

                for asg in asg_response['AutoScalingGroups']:
                    asg_name = asg['AutoScalingGroupName']
                    # asg_name = "onstove-dev-application"
                    asg_desired_count = asg['DesiredCapacity']
                    asg_min_count = asg['MinSize']
                    asg_max_count = asg['MaxSize']
                    print (asg_name)
                    ecs_list = ecs_client.list_clusters()
                    
                    for ecs_arn in ecs_list['clusterArns']:
                        ecs_cluster = ecs_client.describe_clusters(clusters=[ecs_arn])
                        for ecs_name in ecs_cluster['clusterName']:
                            if ecs_name is not none:
                                print (ecs_name)

                        # for ecs_name in ecs_info['clusters'][0]['ClusterName']:
                        #     if ecs_name == asg_name:
                                #print (ecs_name)
                        # if ecs_cn == asg_name:
                        #     cluster_arn = ecs_info['clusterArn']
                        #     print (cluster_arn)
    #                         arn_array = cluster_arn.split("/")
    #                         cluster_name = arn_array[-1]

    #                         svc_list = client2.list_services(clusterName=cluster_name)
    #                         for svc in svc_list:
    #                             svc_arn = svc['serviceArns']

    #                             svc_info = client2.describe_services(clusterName=cluster_name, serviceARN=svc_arn)

    #                             for svc in svc_info:
    #                                 svc_name = services['serviceName']

    #                                 if cluster_name == svc_name:
    #                                     svc_desired_count = svc['desiredCount']
    #                                     svc_running_count = svc['runningCount']
    #                                     svc_pending_count = svc['runningCount']
    #                                 else:
    #                                     logger.info("Not Matched!")
    #                                     svc_desired_count = "-"
    #                                     svc_running_count = "-"
    #                                     svc_pending_count = "-"

    #                                 #append data
                    output.append({
                        "ACCOUNT" : f"'{account}",
                        "ACCOUNT_NAME" : account_name,
                        "REGION" : region,
                        "ASG_NAME" : asg_name
#                                     "ASG_DESIRED_COUNT" : asg_desired_count,
#                                     "ASG_MIN_COUNT" : asg_min_count,
#                                     "ASG_MAX_COUNT" : asg_max_count,
#                                     "SVC_NAME" : svc_name,
#                                     "SVC_DESIRED_COUNT" : svc_desired_count,
#                                     "SVC_MIN_COUNT" : svc_min_count,
#                                     "SVC_MAX_COUNT" : svc_max_count
                    })
    #                                 logger.info(f"{SVC_MAX_COUNT}")

                if 'NextToken' in asg_response:
                    next_token = asg_response['NextToken']
                else:
                    next_token = None

        except Exception as e:
            logger.info("Error!!")
            logger.exception("message")
    
    logger.info(f"{account_name} >> Finish Describing ASG & ECS SVC Desired Count!")
    return output