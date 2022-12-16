import boto3

def ec2(logger,credentials,account,account_name):
    logger.info(f"{account_name} >> Start Describing EC2 Instances...")

    output = []

    region_list = [
        "us-east-1",
        "us-east-2",
        "us-west-1",
        "us-west-2",
        "ap-south-1",
        "ap-northeast-3",
        "ap-northeast-2",
        "ap-southeast-1",
        "ap-southeast-2",
        "ap-northeast-1",
        "ca-central-1",
        "eu-central-1",
        "eu-west-1",
        "eu-west-2",
        "eu-west-3",
        "eu-north-1",
        "sa-east-1"
    ]

    for region in region_list:
        logger.info(f"get in Region - {region} ...")
        try:
        
            client = boto3.client(
                'ec2',
                aws_access_key_id=credentials['AccessKeyId'],
                aws_secret_access_key=credentials['SecretAccessKey'],
                aws_session_token=credentials['SessionToken'],
                region_name = region
            )

            instances_response = ''
            next_token = ''
            first_check = True


            while next_token is not None:
                
                if first_check:
                    instances_response = client.describe_instances()
                    first_check = False
                else:
                    instances_response = client.describe_instances(NextToken=next_token)

                for instances in instances_response['Reservations']:
                    for instance in instances['Instances']:
                        host_name = ''
                        public_ip = ''
                        os_tag = ''
                            
                        if instance["State"]["Name"] == "terminated":
                            continue

                        #get public ip
                        private_ip_addresses = instance['NetworkInterfaces'][0]['PrivateIpAddresses']
                        for private_ip_address in private_ip_addresses:
                            if 'Association' in private_ip_address:
                                public_ip = private_ip_address["Association"]["PublicIp"]
                            else:
                                public_ip = ''
                        
                        #get name
                        for tag in instance['Tags']:
                            if tag['Key'] == 'Name':
                                host_name = tag['Value']
                                break

                        #get os tag
                        for tag in instance['Tags']:
                            if tag['Key'] == 'OS':
                                os_tag = tag['Value']
                                break

                        #append data
                        output.append({
                            "ACCOUNT" : f"'{account}",
                            "ACCOUNT_NAME" : account_name,
                            "REGION" : region,
                            "INSTANCE_NAME" : host_name,
                            "INSTANCE_ID" : instance["InstanceId"],
                            "TYPE" : instance["InstanceType"],
                            "STATE" : instance["State"]["Name"],
                            "VPC" : instance["VpcId"],
                            "SUBNET" : instance["SubnetId"],
                            "PUBLIC_IP" : public_ip,
                            "PRIVATE_IP" : instance["PrivateIpAddress"],
                            "OS Tag" : os_tag
                        })
                if 'NextToken' in instances_response:
                    next_token = instances_response['NextToken']
                else:
                    next_token = None
            
        except Exception as e:
            logger.info("Error!!")
            logger.exception("message")
    
    logger.info(f"{account_name} >> Finish Describing EC2 Instances!")
    return output