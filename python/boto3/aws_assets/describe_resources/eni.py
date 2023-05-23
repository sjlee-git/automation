import boto3

def eni(logger,credentials,account,account_name):
    logger.info(f"{account_name} >> Start Describing ENI Instances...")

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

            interfaces_response = ''
            next_token = ''
            first_check = True

            while next_token is not None:
                
                if first_check:
                    interfaces_response = client.describe_network_interfaces()
                    first_check = False
                else:
                    interfaces_response = client.describe_network_interfaces(NextToken=next_token)

                for interfaces in interfaces_response['NetworkInterfaces']:
                    tag_name = ''
                    public_ip = ''
                    instance_id = ''

                    # get instance id (if 'interfaces' have 'attachment')
                    for attachment in interfaces:
                        if 'Attachment' in interfaces:
                            attachment = interfaces['Attachment']
                            # print(attachment)
                            if 'InstanceId' in attachment:
                                # print(attachment)
                                instance_id = interfaces['Attachment']['InstanceId']
                                # print(instance_id)
                                break
                            else:
                                instance_id = ''        

                    # get public ip
                    private_ip_addresses = interfaces['PrivateIpAddresses']
                    for private_ip_address in private_ip_addresses:
                        if 'Association' in private_ip_address:
                            public_ip = private_ip_address['Association']['PublicIp']
                        else:
                            public_ip = ''

                    # get tag name
                    for tag in interfaces['TagSet']:
                        if tag['Key'] == 'Name':
                            tag_name = tag['Value']
                            break  

                    # append data
                    output.append({
                        # "ACCOUNT" : f"'{account}",
                        "ACCOUNT NAME" : account_name,
                        "REGION" : region,
                        "NAME" : tag_name,
                        "INTERFACE ID" : interfaces['NetworkInterfaceId'],
                        "INTERFACE TYPE" : interfaces['InterfaceType'],
                        "STATUS" : interfaces['Status'],
                        "INSTANCE ID" : instance_id,
                        "PUBLIC IP" : public_ip,
                        "PRIVATE IP" : interfaces['PrivateIpAddress'],
                        # "SECONDARY IP" : interfaces['SecondaryPrivateIpAddressCount'],                      
                        "VPC" : interfaces['VpcId'],
                        "SUBNET" : interfaces['SubnetId'],
                        "DESCRIPTION" : interfaces['Description']
                    })

                if 'NextToken' in interfaces_response:
                    next_token = interfaces_response['NextToken']
                else:
                    next_token = None
            
        except Exception as e:
            logger.info("Error!!")
            logger.exception("message")
    
    logger.info(f"{account_name} >> Finish Describing Network Interfaces!")
    return output