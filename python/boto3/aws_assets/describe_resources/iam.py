import boto3
from datetime import timedelta

def iam(logger,credentials,account,account_name):
    logger.info(f"{account_name} >> Start Describing IAM...")

    output = []

    # IAM Client
    iam_client = boto3.client(
        'iam',
        aws_access_key_id=credentials['AccessKeyId'],
        aws_secret_access_key=credentials['SecretAccessKey'],
        aws_session_token=credentials['SessionToken']
    )


    # IAM User
    response = ''
    next_token = ''
    first_check = True

    while next_token is not None:

        if first_check:
            response = iam_client.list_users()
            first_check = False
        else:
            response = iam_client.list_users(Marker=next_token)

        for user in response['Users']:
            last_used = ''
            # 패스워드 있을 시
            if 'PasswordLastUsed' in user:
                last_used = user['PasswordLastUsed']
            
            # Access key 있을 시
            key_last_used = ''
            try:
                
                key_response = iam_client.list_access_keys(
                    UserName=user["UserName"]
                )
                for key in key_response["AccessKeyMetadata"]:
                    key_id = key["AccessKeyId"]

                    key_last_used_response = iam_client.get_access_key_last_used(
                        AccessKeyId=key_id
                    )
                    if key_last_used == '':
                        key_last_used = key_last_used_response["AccessKeyLastUsed"]["LastUsedDate"]
                    else:
                        if key_last_used < key_last_used_response["AccessKeyLastUsed"]["LastUsedDate"]:
                            key_last_used = key_last_used_response["AccessKeyLastUsed"]["LastUsedDate"]

            except Exception as e:
                            logger.info("Error!!")
                            logger.exception("message")
            
            if last_used == '':
                last_used = key_last_used
            else:
                if key_last_used != '':
                    if last_used < key_last_used : last_used = key_last_used


            #시간 변환
            created_date = user["CreateDate"]
            if created_date != '':
                created_date = (created_date-timedelta(hours=-9)).strftime("%Y-%m-%d %H:%M")

            if last_used != '':
                last_used = (last_used-timedelta(hours=-9)).strftime("%Y-%m-%d %H:%M")

            #append to output
            output.append({
                "ACCOUNT" : f"'{account}",
                "Account Name" : account_name,
                "User/Role" : "User",
                "Name" : user["UserName"],
                "Arn" : user["Arn"],
                "Created Date" : created_date,
                "Last Activity" : last_used
            })

        if 'Marker' in response:
            next_token = response['Marker']
        else:
            next_token = None

    # IAM Role
    # response = ''
    # next_token = ''
    # first_check = True


    # while next_token is not None:

    #     if first_check:
    #         response = iam_client.list_roles()
    #         first_check = False
    #     else:
    #         response = iam_client.list_roles(Marker=next_token)


    #     for role in response['Roles']:

    #         last_used = ''

    #         role_response = iam_client.get_role(
    #             RoleName=role["RoleName"]
    #         )
    #         if "LastUsedDate" in role_response["Role"]["RoleLastUsed"]:
    #             last_used = role_response["Role"]["RoleLastUsed"]["LastUsedDate"]

    #         #시간 변환
    #         created_date = role["CreateDate"]
    #         if created_date != '':
    #             created_date = (created_date-timedelta(hours=-9)).strftime("%Y-%m-%d %H:%M")

    #         if last_used != '':
    #             last_used = (last_used-timedelta(hours=-9)).strftime("%Y-%m-%d %H:%M")
            
    #         #append to output
    #         output.append({
    #             "ACCOUNT" : account,
    #             "Account Name" : account_name,
    #             "User/Role" : "Role",
    #             "Name" : role["RoleName"],
    #             "Arn" : role["Arn"],
    #             "Created Date" : created_date,
    #             "Last Activity" : last_used
    #         })

    #     if 'Marker' in response:
    #         next_token = response['Marker']
    #     else:
    #         next_token = None
    
    logger.info(f"{account_name} >> Finish Describing IAM...")
    return output