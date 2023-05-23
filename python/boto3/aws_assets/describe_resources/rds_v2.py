import boto3

def rds_v2(logger,credentials,account,account_name):
    logger.info(f"{account_name} >> Start Describing RDS Instances...")

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
                'rds',
                aws_access_key_id = credentials['AccessKeyId'],
                aws_secret_access_key = credentials['SecretAccessKey'],
                aws_session_token = credentials['SessionToken'],
                region_name = region
            )

            instances_response = ''
            next_token = ''
            first_check = True

            while next_token is not None:
                
                if first_check:
                    instances_response = client.describe_db_instances()
                    first_check = False
                else:
                    instances_response = client.describe_db_instances(NextToken=next_token)
                engine = ''
                engine_v = ''
                name = ''
                for instances in instances_response['DBInstances']:

                    engine = instances["Engine"]
                    engine_v = instances["EngineVersion"]
                    name = instances["DBInstanceIdentifier"]

                    # append data
                    output.append({
                        "ACCOUNT" : f"'{account}",
                        "ACCOUNT_NAME" : account_name,
                        "REGION" : region,
                        "RDS NAME" : name,
                        "ENGINE" : engine,
                        "ENGINE VERSION" : engine_v
                    })
                if 'NextToken' in instances_response:
                    next_token = instances_response['NextToken']
                else:
                    next_token = None
            
        except Exception as e:
            logger.info("Error!!")
            logger.exception("message")
    
    logger.info(f"{account_name} >> Finish Describing RDS Instances!")
    return output