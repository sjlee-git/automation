import boto3

def temp(logger,credentials,account,account_name):
    logger.info(f"{account_name} >> Start Describing {temp.__name__}...")

    output = []

    client = boto3.client(
        'ec2',
        aws_access_key_id=credentials['AccessKeyId'],
        aws_secret_access_key=credentials['SecretAccessKey'],
        aws_session_token=credentials['SessionToken']
    )

    try:
        response = client.describe_instances()

        output.append({
            "ACCOUNT" : f"'{account}",
            "ACCOUNT_NAME" : account_name,
            "data" : response["data"]
        })
    except Exception as e:
        logger.info("Error!!")
        logger.exception("message")
    
    
    logger.info(f"{account_name} >> Finish Describing {temp.__name__}...")
    return output