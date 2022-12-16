import boto3

def get_session(key,account,account_type):

    session = boto3.Session()
    
    role_arn = ''

    if account_type == "game" or account == "802695694910":
        role_arn = "arn:aws:iam::"+account+":role/mgmt_infra"
    elif account_type == "platform":
        role_arn = "arn:aws:iam::"+account+":role/console-mgmt-admin"

    

    sts_client = session.client(
        'sts',
        aws_access_key_id=key["KEY_ID"],
        aws_secret_access_key=key["SECRET_KEY"]
    )
    assumed_role = sts_client.assume_role(
        RoleArn=role_arn,
        RoleSessionName="switchrole1"
    )
    credentials = assumed_role['Credentials']
    
    return credentials