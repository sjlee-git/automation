import boto3

def elasticache(logger,credentials,account,account_name):
    logger.info(f"{account_name} >> Start Describing ElastiCache (Redis) ...")

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
        logger.info(f"get in Region - {region} ...")
        try:
            client = boto3.client(
                'elasticache',
                aws_access_key_id = credentials['AccessKeyId'],
                aws_secret_access_key = credentials['SecretAccessKey'],
                aws_session_token = credentials['SessionToken'],
                region_name = region
            )

            cache_response = client.describe_cache_clusters()
            for cache in cache_response['CacheClusters']:
                cluster_name = cache['CacheClusterId']
                engine = cache['Engine']
                engine_version = cache['EngineVersion']
                node_type = cache['CacheNodeType']

                # append data
                output.append({
                    # "ACCOUNT" : f"'{account}",
                    "ACCOUNT NAME" : account_name,
                    "REGION" : region,
                    "CLUSTER NAME" : cluster_name,
                    "ENGINE" : engine,
                    "ENGINE VERSION" : engine_version,
                    "NODE TYPE" : node_type
                })
        except Exception as e:
            logger.info("Error!!")
            logger.exception("message")

    
    logger.info(f"{account_name} >> Finish Describing ElastiCache (Redis) ...")
    return output