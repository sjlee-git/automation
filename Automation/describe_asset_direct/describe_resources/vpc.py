import boto3

### 리소스 Describe 용도 Template 코드 입니다.
### 필요에 따라 client 정보와 response에서 가져올 Data 정보를 수정해야 합니다.
### Output은 Dict 로 이루어진 List 자료구조로 return 해야 정상 동작합니다.
### Dict의 Key 값은 해당 Data의 식별자로서 Export 될 때 CSV 파일의 상단 Column 명이 됩니다.


def vpc(logger,credentials,account,account_name):
    logger.info(f"{account_name} >> Start Describing {vpc.__name__}...")

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

        client = boto3.client(
            'ec2',
            aws_access_key_id=credentials['AccessKeyId'],
            aws_secret_access_key=credentials['SecretAccessKey'],
            aws_session_token=credentials['SessionToken'],
            region_name = region
        )

        try:
            response_list = client.describe_vpcs(
                Filters=[
                    {
                        'Name': 'owner-id',
                        'Values': [
                            account
                        ]
                    }
                ]
            )['Vpcs']

            for response in response_list:
                name = ''
                #get name
                if 'Tags' in response:
                    for tag in response['Tags']:
                        if tag['Key'] == 'Name':
                            name = tag['Value']
                            break

                output.append({
                    "ACCOUNT" : f"'{account}",
                    "ACCOUNT_NAME" : account_name,
                    "Region" : region,
                    "VpcId" : response["VpcId"],
                    "Name" : name,
                    "cidr" : response["CidrBlock"]
                })
        
        except Exception as e:
            logger.info("Error!!")
            logger.exception("message")

    
    logger.info(f"{account_name} >> Finish Describing {vpc.__name__}...")
    return output