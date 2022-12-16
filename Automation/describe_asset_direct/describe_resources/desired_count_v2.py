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

            client2 = boto3.client(
                'ecs',
                aws_access_key_id=credentials['AccessKeyId'],
                aws_secret_access_key=credentials['SecretAccessKey'],
                aws_session_token=credentials['SessionToken'],
                region_name = region
            )

            asg_response = ''
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
                    asg_desired_count = asg['DesiredCapacity']
                    asg_min_count = asg['MinSize']
                    asg_max_count = asg['MaxSize']

                    cluster_list = []
                    
                    for cluster in client2.list_clusters().get('clusterArns'):
                        cluster_name = str(cluster).split('/')[-1]
                        
                        if asg_name == cluster_name:
                        #if asg_name in cluster_name:
                            cluster_list.append(cluster_name)
                            client2.describe_clusters(clusters=cluster_list).get('clusters')

                            # service_count = len(client2.list_services(
                            #         cluster=cluster_name
                            #     ).get('serviceArns')
                            # )

                            service_arns = client2.list_services(
                                cluster=cluster_name
                            ).get('serviceArns')

                            if service_arns:
                                service_names = client2.describe_services(cluster=cluster_name, services=service_arns).get('services')
                                for service in service_names:
                                    # Service Name, Service Status, Launch Type, Service Created Date
                                    svc_name = service.get('serviceName')  # Service Name
                                    svc_desired_count = service.get('desiredCount')
                                    svc_running_count = service.get('runningCount')
                                    svc_pending_count = service.get('pendingCount')
                                    svc_status = str(service.get('status')).lower().capitalize()

                                    #append data
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

                        else:
                            logger.info(f"There is no '{cluster_name}' ECS Cluster with the same name as '{asg_name}' ASG.")

                if 'NextToken' in asg_response:
                    next_token = asg_response['NextToken']
                else:
                    next_token = None

        except Exception as e:
            logger.info("Error!!")
            logger.exception("message")
    
    logger.info(f"{account_name} >> Finish Describing ASG & ECS SVC Desired Count!")
    return output