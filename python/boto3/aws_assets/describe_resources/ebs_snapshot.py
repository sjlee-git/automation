import boto3

def snapshot(logger,credentials,account,account_name):
    logger.info(f"{account_name} >> Start Describing EBS Snapshot...")

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

            response = ''
            next_token = ''
            first_check = True


            while next_token is not None:
                
                if first_check:
                    response = client.describe_snapshots(
                        OwnerIds=[
                            account,
                        ]
                    )
                    first_check = False
                else:
                    response = client.describe_snapshots(
                        OwnerIds=[
                            account,
                        ],
                        NextToken=next_token
                    )

                for snapshot in response['Snapshots']:
                    #append data
                    output.append({
                        "ACCOUNT" : f"'{account}",
                        "ACCOUNT_NAME" : account_name,
                        "REGION" : region,
                        "SNAPSHOT_ID" : snapshot["SnapshotId"],
                        "VOLUME_ID" : snapshot["VolumeId"],
                        "SIZE" : snapshot["VolumeSize"],
                        "TIER" : snapshot["StorageTier"],
                        "STATUS" : snapshot["State"],
                        "STARTED" : snapshot["StartTime"],
                        "DESCRIPTION" : snapshot["Description"]
                    })
                if 'NextToken' in response:
                    next_token = response['NextToken']
                else:
                    next_token = None
            
        except Exception as e:
            logger.info("Error!!")
            logger.exception("message")
    
    
    logger.info(f"{account_name} >> Finish Describing EBS Snapshot...")
    return output