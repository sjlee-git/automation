import boto3

def route53(logger,credentials,account,account_name):
    logger.info(f"{account_name} >> Start Describing route53...")
    output = []
    client = boto3.client(
        'route53',
        aws_access_key_id=credentials['AccessKeyId'],
        aws_secret_access_key=credentials['SecretAccessKey'],
        aws_session_token=credentials['SessionToken']
    )
    pagenate_hosted_zone = client.get_paginator('list_hosted_zones')
    pagenate_record_sets = client.get_paginator('list_resource_record_sets')

    for zone_page in pagenate_hosted_zone.paginate():
        for zone in zone_page['HostedZones']:
            zone_name = zone['Name']
            zone_id = zone['Id']
            zone_config = zone['Config']['PrivateZone']
            if zone_config == True:
                zone_configtype = 'Private'
            else:
                zone_configtype = 'Public'
            for record_page in pagenate_record_sets.paginate(HostedZoneId=zone_id):
                for record in record_page['ResourceRecordSets']:
                    record_name = record['Name'],
                    record_type = record['Type'],
                    routing_policy = ''
                    differentiator = ''
                    if "Weight" in record:
                        routing_policy = "Weighted"
                        differentiator = record['Weight']
                    elif "GeoLocation" in record:
                        routing_policy = "GeoLocation"
                        try :
                            differentiator = record['GeoLocation']['CountryCode']
                        except Exception as e:
                            differentiator = 'Default'
                    elif "Failover" in record:
                        routing_policy = "Failover"
                        differentiator = record['Failover']
                    elif "CidrRoutingConfig" in record:
                        routing_policy = "IP-based"
                        if record['CidrRoutingConfig']['LocationName'] == "*":
                            differentiator = "Default"
                        else:
                            differentiator = record['CidrRoutingConfig']['LocationName']
                    elif "Region" in record:
                        routing_policy = "Latency"
                        differentiator = '-'
                    elif "MultiValueAnswer" in record:
                        if record['MultiValueAnswer'] == "True":
                            routing_policy = "Multi Value Answer"
                    else:
                        routing_policy = "Simple"
                        differentiator = '-'
                    if "ResourceRecords" in record:
                        record_values = record['ResourceRecords']
                        record_value_len = len(record_values)
                        for e in range(record_value_len):
                            record_value = record_values[e]
                            output.append({
                                "ACCOUNT" : f"'{account}",
                                "ACCOUNT_NAME" : account_name,
                                "HOST_TYPE" : zone_configtype,
                                "HOST_ZONE" : zone_name,
                                "RECORD" : record_name,
                                "TYPE" : record_type,
                                "ROUTING_POLICY" : routing_policy,
                                "DIFFERENTIATOR" : differentiator,
                                "VALUE" : record_value
                            })
                    elif 'AliasTarget' in record:
                        record_values = record['AliasTarget']['DNSName']
                        output.append({
                            "ACCOUNT" : f"'{account}",
                            "ACCOUNT_NAME" : account_name,
                            "HOST_TYPE" : zone_configtype,
                            "HOST_ZONE" : zone_name,
                            "RECORD" : record_name,
                            "TYPE" : record_type,
                            "ROUTING_POLICY" : routing_policy,
                            "DIFFERENTIATOR" : differentiator,
                            "VALUE" : record_values
                        })
    logger.info(f"{account_name} >> Finish Describing route53...")
    return output