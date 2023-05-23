import boto3

def cloudfront(logger,credentials,account,account_name):
    logger.info(f"{account_name} >> Start Describing cloudfront...")

    output = []

    client = boto3.client(
        'cloudfront',
        aws_access_key_id=credentials['AccessKeyId'],
        aws_secret_access_key=credentials['SecretAccessKey'],
        aws_session_token=credentials['SessionToken']
    )

    try:
        response = ''
        next_token = ''
        first_check = True


        while next_token is not None:
            if first_check:
                response = client.list_distributions()['DistributionList']
                first_check = False
            else:
                response = client.list_distributions(Marker=next_token)['DistributionList']

            for item in response['Items']:
                alias = ''
                if item['Aliases']['Quantity'] > 0:
                    for al in item['Aliases']['Items']:
                        if alias == '':
                            alias = al
                        else:
                            alias = alias + ", " + al
                else:
                    alias = '-'
                
                origins = ''
                if item['Origins']['Quantity'] > 0:
                    for origin in item['Origins']['Items']:
                        if origins == '':
                            origins = origin['DomainName']
                        else:
                            origins = origins + ", " + origin['DomainName']
                else:
                    origins = '-'

                output.append({
                    "ACCOUNT" : f"'{account}",
                    "ACCOUNT_NAME" : account_name,
                    "id" : item["Id"],
                    "Description" : item["Comment"],
                    "DomainName" : item["DomainName"],
                    "Aliases" : alias,
                    "Origins" : origins,
                    "WebACLId" : item["WebACLId"]
                })
            
            if 'NextMarker' in response:
                next_token = response['NextMarker']
            else:
                next_token = None
    except Exception as e:
                logger.info("Error!!")
                logger.exception("message")

    
    logger.info(f"{account_name} >> Finish Describing cloudfront...")
    return output