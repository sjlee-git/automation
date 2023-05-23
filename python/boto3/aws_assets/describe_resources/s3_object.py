import boto3

def s3_object(logger,credentials,account,account_name):
    logger.info(f"{account_name} >> Start Describing S3...")
    output = []
    client = boto3.client(
        's3',
        aws_access_key_id=credentials['AccessKeyId'],
        aws_secret_access_key=credentials['SecretAccessKey'],
        aws_session_token=credentials['SessionToken'],
        )
    bucket_response = client.list_buckets()
    for bucket in bucket_response['Buckets']:
        bucket_name = bucket['Name']
        print (bucket_name)
        obj_paginator = client.get_paginator('list_objects_v2')
        obj_responses = obj_paginator.paginate(
            Bucket=[bucket_name],
            PaginationConfig={
                'PageSize' : 10
            }
        )
        for obj_response in obj_responses():
            for obj in obj_response['Contents']:
                obj_date = obj['LastModified']
                output.append({
                    "ACCOUNT_NAME" : account_name,
                    "BUCKET_NAME" : bucket_name,
                    "OBJECT_DATE" : obj_date,
                })
    logger.info(f"{account_name} >> Finish Describing S3...")
    return output