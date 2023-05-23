import os
import set_logger
import configparser
import switch_role
from describe_resources import ebs_snapshot,ec2,iam,maintenance,cloudfront,vpc,subnet,eip,security,desired_count,cache,rds,security_in
from datetime import datetime
import export_csv

if __name__ == '__main__':

    ## Get File Path
    abs_file_path = os.path.abspath(__file__)
    file_path = os.path.split(abs_file_path)[0]

    ## Set Logger
    logger = set_logger.set_logger(file_path)
    
    ## Read Config
    conf = configparser.ConfigParser()
    conf.read(file_path + "/config.ini", encoding='utf-8')



    ## Start
    logger.info("Start Script")

    # Set Target Accounts
    platform_account_list = conf['PLATFORM_ACCOUNTS']
    game_account_list = conf['GAME_ACCOUNTS']
    
    # 플랫폼, 게임 Account 대상 입력
    target_input = input("계정 대상 종류를 입력하세요.(숫자만 입력)\n1.플랫폼 2.모바일게임 3.전체 :")
    target = []
    if target_input == '1':
        target.append(platform_account_list)
    elif target_input == '2':
        target.append(game_account_list)
    elif target_input == '3':
        target.append(platform_account_list)
        target.append(game_account_list)
    else:
        logger.info("알 수 없는 input 입니다.")
        logger.info("Script 비정상 종료")
        quit()

    
    ## Get Data

    # 서비스 대상 입력
    # 신규 서비스 describe 메소드 추가 시 아래 분기문에 추가
    service_input = input("추출할 서비스 선택.(숫자만 입력)\n"
                            "1.EC2\n"
                            "2.VPC\n"
                            "3.Subnet\n"
                            "4.CloudFront\n"
                            "5.Maintenance\n"
                            "6.EBS Snapshot\n"
                            "7.IAM\n"
                            "8.EIP\n"
                            "9.Securitygroups\n"
                            "10.Service Count\n"
                            "11.mainteanace_cachce\n"
                            "12.RDS\n"
                            "13.Security Insert\n"
                            ":")
    
    call_method = None

    if service_input == '1':
        call_method = ec2.ec2
    elif service_input == '2':
        call_method = vpc.vpc
    elif service_input == '3':
        call_method = subnet.subnet
    elif service_input == '4':
        call_method = cloudfront.cloudfront
    elif service_input == '5':
        call_method = maintenance.maintenance
    elif service_input == '6':
        call_method = ebs_snapshot.snapshot
    elif service_input == '7':
        call_method = iam.iam
    elif service_input == '8':
        call_method = eip.eip
    elif service_input == '9':
        call_method = security.security
    elif service_input == '10':
        call_method = desired_count.count
    elif service_input == '11':
        call_method = cache.cache
    elif service_input == '12':
        call_method = rds.rds
    elif service_input == '13':
        call_method = security_in.security_in
    else:
        logger.info("알 수 없는 input 입니다.")
        logger.info("Script 비정상 종료")
        quit()

    # 선택한 대상 계정과 서비스로 전체 리소스 가져오기
    data_list = []
    for account_list in target:

        for account in account_list:
            account_name = account_list[account]
            logger.info(f'Target Account : {account_name}({account})...')

            account_type = ''
            if account_list == platform_account_list:
                account_type = 'platform'
            elif account_list == game_account_list:
                account_type = 'game'
            
            ## Get Credential
            master_key = conf["MASTER_ACCESS_KEY"]
            credentials = switch_role.get_session(master_key,account,account_type)

            ## Get Data
            try:
                return_data = call_method(logger,credentials,account,account_name)

                # insert data
                data_list.extend(return_data)

            except Exception as e:
                logger.info("Error!!")
                logger.exception("message")

    logger.info("Finish Describing")

    ## Export CSV
    logger.info("Export CSV...")
    now_time = datetime.now().strftime('_%Y-%m-%d_%H%M%S')

    output_file_name = "output_" + call_method.__name__
    output_file = file_path + '/output/' + output_file_name + now_time + ".csv"
    export_csv.export_by_csv(output_file,data_list)
    logger.info(f"Saved... {output_file}")

    ## Finish
    logger.info("Finish Script")