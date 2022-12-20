#!/bin/bash

CLB_NAME="TestCLB"
PROFILE_NAME="MyProfile"

status()
{
    # 1. CLB에 등록된 Instance를 배열로 저장
    instances=$(aws --profile ${PROFILE_NAME} elb describe-load-balancers \
    --load-balancer-name ${CLB_NAME} --query \
    'LoadBalancerDescriptions[].Instances[].{Id: InstanceId}' --output text)

    echo "Current Instances attached to CLB ${CLB_NAME}"
    cnt=1
        # instance를 반복문 돌음
    for instance_id in $instances; do

                # 상태 확인 (InService | OutOfService | Unknown)
                health_status=$(aws --profile ${PROFILE_NAME} elb describe-instance-health \\
                --load-balancer-name ${CLB_NAME} \\
                --instances ${instance_id} \\
                --query 'InstanceStates[].State' --output text)
                instance_name=$(aws ec2 describe-tags --profile ${PROFILE_NAME} \\
                --filters Name=resource-id,Values=${instance_id} Name=key,Values=Name \\
                --query "Tags[].Value" --output text)

        echo "Instance ${cnt} : ${instance_id}, Health : ${health_status} (${instance_name})"
        cnt=`expr $cnt + 1`
    done
}

# 사용법
usage()
{
        echo "==================Usage=================="
        echo "$0 -a {instance_id} | -d {instance_id} | -s"
        echo "<Options>"
        echo "  -a {instance_id}"
        echo "     : attach instance to classic load balancer ${CLB_NAME}"
        echo "  -d {instance_id}"
        echo "     : detach instance from classic load balancer ${CLB_NAME}"
        echo "  -s : Show attached instanced to classic load balancer ${CLB_NAME}"
        echo "  -h : Show help message"
        exit 1
}

attach()
{
        # Instance id가 OPTARG에 의해 attach 함수로 넘어온다.
        aws --profile ${PROFILE_NAME} elb register-instances-with-load-balancer \\
        --load-balancer-name ${CLB_NAME} \\
        --instances $instance_id
}

detach()
{
        # Instance id가 OPTARG에 의해 detach 함수로 넘어온다.
        aws --profile ${PROFILE_NAME} elb deregister-instances-from-load-balancer \\
    	--load-balancer-name ${CLB_NAME} \\
    	--instances $instance_id
}

while getopts a:d:sh opts; do
        case $opts in
        a)
                instance_id="${OPTARG}"
                if [[ -n "$instance_id" ]]; then
                        attach
                else
                        echo "You need to specify instasnce id."
                        echo ""
                        usage
                fi
                ;;
        d)
                instance_id="${OPTARG}"
                detach
                ;;
        s)
                status
                ;;
        h)
                usage
                ;;
        esac
done