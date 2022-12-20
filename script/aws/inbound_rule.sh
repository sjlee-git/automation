#!/bin/bash

## Describe Security Group
#aws ec2 describe-security-groups --group-ids sg-0000000000000000

## Add Inbound rule to Security Group
# aws ec2 authorize-security-group-ingress \
#     --group-id sg-0000000000000000 \
#     --ip-permissions IpProtocol=tcp,FromPort=80,ToPort=443,IpRanges='[{CidrIp='${CIDR}/32',Description='${DESC}'}]'

## Variables
while read line; do
    echo ${line}
    # add inbound rule to security group
    aws ec2 authorize-security-group-ingress \
    --group-id sg-0000000000000000 \
    --ip-permissions IpProtocol=tcp,FromPort=80,ToPort=443,IpRanges='[{CidrIp='${line}/32',Description='ISRIR-20730'}]'
done < source.txt

value=$(<source.txt)
echo ${value}

for var in ${value}
do
    echo ${var}
    # add inbound rule to security group
    aws ec2 authorize-security-group-ingress \
    --group-id sg-0000000000000000 \
    --ip-permissions IpProtocol=tcp,FromPort=80,ToPort=443,IpRanges='[{CidrIp='${var}/32',Description='ISRIR-20730'}]'   
done