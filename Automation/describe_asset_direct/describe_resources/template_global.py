import boto3

### 리소스 Describe 용도 Template 코드 입니다.
### 필요에 따라 client 정보와 response에서 가져올 Data 정보를 수정해야 합니다.
### 특정 Region 에 대해 가져와야 할 시 client 에 region 정보를 주어 client를 호출해야합니다.
### Output은 Dict 로 이루어진 List 자료구조로 return 해야 정상 동작합니다.
### Dict의 Key 값은 해당 Data의 식별자로서 Export 될 때 CSV 파일의 상단 Column 명이 됩니다.


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