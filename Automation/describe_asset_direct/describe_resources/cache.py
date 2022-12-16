import boto3

def cache(logger,credentials,account,account_name):
    logger.info(f"{account_name} >> Start Describing maintenance...")

    output = []

    health_client = boto3.client(
        'health',
        aws_access_key_id=credentials['AccessKeyId'],
        aws_secret_access_key=credentials['SecretAccessKey'],
        aws_session_token=credentials['SessionToken'],
        region_name = "us-east-1"
    )
    
    event_response = ''
    event_next_token = ''
    first_check = True
    
    while event_next_token is not None:
        if first_check:
            event_response = health_client.describe_events(
                filter={
                    'eventTypeCategories': ['accountNotification'],
                    'services': ['ELASTICACHE']
                }
            )
            first_check = False
        else:
            event_response = health_client.describe_events(
                filter={
                    'eventTypeCategories': ['accountNotification'],
                    'services': ['ELASTICACHE']
                },
                nextToken=event_next_token
            )
        for event in event_response["events"]:
            entity_responses = ''
            entity_next_token  = ''
            enti_first_check = True
            while entity_next_token is not None:
                if enti_first_check:
                    entity_responses = health_client.describe_affected_entities(
                        filter={
                            'eventArns': [
                                event["arn"]
                            ]
                        }
                    )
                    enti_first_check= False
                else:
                    entity_responses = health_client.describe_affected_entities(
                        filter={
                                'eventArns': [
                                    event["arn"]
                                ]
                            },
                            nextToken=entity_next_token
                    )
                for entity_response in entity_responses["entities"]:
                    try:
                        affected_entity = entity_response["entityValue"]
                        ec_client = boto3.client(
                            'elasticache',
                            aws_access_key_id=credentials['AccessKeyId'],
                            aws_secret_access_key=credentials['SecretAccessKey'],
                            aws_session_token=credentials['SessionToken'],
                            region_name = event['region'])
                        cacheinfo = ec_client.describe_cache_clusters(
                            CacheClusterId = affected_entity
                        )
                        cache_engine = cacheinfo["CacheClusters"][0]["Engine"]
                        cache_v = cacheinfo["CacheClusters"][0]["EngineVersion"]
                        node = cacheinfo["CacheClusters"][0]["CacheNodeType"]
                    except Exception as e:
                        try:
                            rginfo = ec_client.describe_replication_groups(
                                ReplicationGroupId = affected_entity
                            )
                            for gids in rginfo["ReplicationGroups"][0]["NodeGroups"][0]["NodeGroupMembers"]:
                                gid = gids["CacheClusterId"]
                                cacheinfo = ec_client.describe_cache_clusters(
                                CacheClusterId = gid
                                )
                                cache_engine = cacheinfo["CacheClusters"][0]["Engine"]
                                cache_v = cacheinfo["CacheClusters"][0]["EngineVersion"]
                                node = cacheinfo["CacheClusters"][0]["CacheNodeType"]
                        except Exception as e:
                            continue
                            logger.info("Error!!")
                            logger.exception("message")
                    output.append({
                        "ACCOUNT" : f"'{account}",
                        "ACCOUNT_NAME" : account_name,
                        "Service" : event["service"],
                        "Event Type Category" : event["eventTypeCode"],
                        "Start Time" : event["startTime"],
                        "Region" : event["region"],
                        "Affected entities" : affected_entity,
                        "Engine" : cache_engine,
                        "Version" : cache_v,
                        "NodeType" : node
                        })
                    if 'nextToken' in entity_responses:
                        entity_next_token = entity_responses['nextToken']
                    else:
                        entity_next_token = None
        if 'nextToken' in event_response:
            event_next_token = event_response['nextToken']
        else:
            event_next_token = None
    
    logger.info(f"{account_name} >> Finish Describing maintenance...")
    return output