import boto3

def tgw(logger,credentials,account,account_name):
    logger.info(f"{account_name} >> Start Describing TGW...")
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
            region_name=region
        )
        tgw_response = client.describe_transit_gateways()
        
        for tgw in tgw_response['TransitGateways']:
            tgw_id = tgw['TransitGatewayId']
            own_id = tgw['OwnerId']
            if own_id == account:
                tgw_type = 'Owner'
                for tgw_tag in tgw['Tags']:
                    if tgw_tag['Key'] == 'Name':
                        tgw_name = tgw_tag['Value']
            else:
                tgw_type = 'Shared'
                tgw_name = '-'

            att_paginator = client.get_paginator('describe_transit_gateway_attachments')
            att_responses = att_paginator.paginate(
                Filters = [
                    {
                        'Name': 'transit-gateway-id',
                        'Values': [tgw_id]
                    }
                ]
            )
            for att_response in att_responses:
                for tgw_att in att_response['TransitGatewayAttachments']:
                    att_id = tgw_att['TransitGatewayAttachmentId']
                    att_type = tgw_att['ResourceType']
                    att_own = tgw_att['ResourceOwnerId']
                    att_resource = tgw_att['ResourceId']
                    if att_type == 'peering':
                        peer_att = client.describe_transit_gateway_peering_attachments(
                            TransitGatewayAttachmentIds=[att_id]
                        )
                        for peer_response in peer_att['TransitGatewayPeeringAttachments']:
                            if account == peer_response['RequesterTgwInfo']['OwnerId']:
                                if region == peer_response['RequesterTgwInfo']['Region']:
                                    att_region = peer_response['AccepterTgwInfo']['Region']
                                else:
                                    att_region = peer_response['RequesterTgwInfo']['Region']
                            else:
                                att_region = peer_response['RequesterTgwInfo']['Region']
                    else:
                        att_region = region
                    for att_tag in tgw_att['Tags']:
                        if att_tag['Key'] == 'Name':
                            att_name = att_tag['Value']
                            output.append({
                                "ACCOUNT_NAME" : account_name,
                                "REGION" : region,
                                "TGW_ID" : tgw_id,
                                "TGW_NAME" : tgw_name,
                                "TGW_TYPE" : tgw_type,
                                "RESOURCE_TYPE" : att_type,
                                "CONNECTION_NAME" : att_name,
                                "REGION_ATT" : att_region,
                                "RESOURCE_ID" : att_resource
                            })


    # for zone_page in pagenate_hosted_zone.paginate():
    #     for zone in zone_page['HostedZones']:
    #         zone_name = zone['Name']
    #         zone_id = zone['Id']
    #         zone_config = zone['Config']['PrivateZone']
    #         if zone_config == True:
    #             zone_configtype = 'Private'
    #         else:
    #             zone_configtype = 'Public'
    #         for record_page in pagenate_record_sets.paginate(HostedZoneId=zone_id):
    #             for record in record_page['ResourceRecordSets']:
    #                 record_name = record['Name'],
    #                 record_type = record['Type'],
    #                 routing_policy = ''
    #                 differentiator = ''
    #                 if "Weight" in record:
    #                     routing_policy = "Weighted"
    #                     differentiator = record['Weight']
    #                 elif "GeoLocation" in record:
    #                     routing_policy = "GeoLocation"
    #                     try :
    #                         differentiator = record['GeoLocation']['CountryCode']
    #                     except Exception as e:
    #                         differentiator = 'Default'
    #                 elif "Failover" in record:
    #                     routing_policy = "Failover"
    #                     differentiator = record['Failover']
    #                 elif "CidrRoutingConfig" in record:
    #                     routing_policy = "IP-based"
    #                     if record['CidrRoutingConfig']['LocationName'] == "*":
    #                         differentiator = "Default"
    #                     else:
    #                         differentiator = record['CidrRoutingConfig']['LocationName']
    #                 elif "Region" in record:
    #                     routing_policy = "Latency"
    #                     differentiator = '-'
    #                 elif "MultiValueAnswer" in record:
    #                     if record['MultiValueAnswer'] == "True":
    #                         routing_policy = "Multi Value Answer"
    #                 else:
    #                     routing_policy = "Simple"
    #                     differentiator = '-'
    #                 if "ResourceRecords" in record:
    #                     record_values = record['ResourceRecords']
    #                     record_value_len = len(record_values)
    #                     for e in range(record_value_len):
    #                         record_value = record_values[e]
    #                         output.append({
    #                             "ACCOUNT" : f"'{account}",
    #                             "ACCOUNT_NAME" : account_name,
    #                             "HOST_TYPE" : zone_configtype,
    #                             "HOST_ZONE" : zone_name,
    #                             "RECORD" : record_name,
    #                             "TYPE" : record_type,
    #                             "ROUTING_POLICY" : routing_policy,
    #                             "DIFFERENTIATOR" : differentiator,
    #                             "VALUE" : record_value
    #                         })
                    # elif 'AliasTarget' in record:
                    #     record_values = record['AliasTarget']['DNSName']

    logger.info(f"{account_name} >> Finish Describing TGW...")
    return output