import boto3

def security(logger,credentials,account,account_name):
    logger.info(f"{account_name} >> Start Describing Security Groups...")

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

            sg_response = ''
            next_token = ''
            first_check = True


            while next_token is not None:
                
                if first_check:
                    sg_response = client.describe_security_groups()
                    first_check = False
                else:
                    sg_response = client.describe_security_groups(NextToken=next_token)

                for security_groups in sg_response['SecurityGroups']:
                    vpc_id = security_groups['VpcId']
                    for inbound_rules in security_groups['IpPermissions']:
                        ip_type = '-'
                        port_ranges = '-'
                        if inbound_rules['IpProtocol'] == "-1":
                            ip_type = "ALL Traffic"
                            port_ranges = "ALL"
                        else:
                            ip_type = inbound_rules['IpProtocol']
                            if "icmp" in ip_type:
                                port_ranges = "N/A"
                            elif inbound_rules.get('FromPort') == inbound_rules.get('ToPort'):
                                port_ranges = inbound_rules.get('FromPort')
                            else:
                                port_ranges = f"{inbound_rules.get('FromPort')} - {inbound_rules.get('ToPort')}"
                        for ip_range in inbound_rules['IpRanges']:
                            ip_cidr = ['']
                            dest = ['61.111.58.25/32', '61.111.58.26/32']
                            if ip_range['CidrIp'] in dest:
                                vpcinfo = client.describe_vpcs(
                                        Filters=[{"Name":"vpc-id", "Values":[vpc_id]}]
                                )
                                vpcip = vpcinfo['Vpcs'][0]['CidrBlock']
                                #append data
                                output.append({
                                    "ACCOUNT" : f"'{account}",
                                    "ACCOUNT_NAME" : account_name,
                                    "REGION" : region,
                                    "VPC ID" : vpc_id,
                                    "VPC Cidr" : vpcip,
                                    "Protocol" : ip_type,
                                    "Port" : port_ranges,
                                    "Source IP" : ip_range
                                })
                if 'NextToken' in sg_response:
                    next_token = sg_response['NextToken']
                else:
                    next_token = None
            
        except Exception as e:
            logger.info("Error!!")
            logger.exception("message")
    
    logger.info(f"{account_name} >> Finish Describing Security Groups!")
    return output