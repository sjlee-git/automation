#!/bin/bash

GROUP=<resource_group>
NSG_NAME=<security_group>
RULE_NAME=<rule_name>
SRC_IP='0.0.0.0'
DST_IP='0.0.0.0'
PRIORITY="0000"
PROTOCOL="TCP"

az account set -s "subscription"

echo "Create NSG WFH Rule"
az network nsg rule create -g ${GROUP} \
  --nsg-name ${NSG_NAME} --priority ${PRIORITY} \
  -n ${PRIORITY}-in-${PROTOCOL,,}-${RULE_NAME}-a \
  --source-address-prefixes ${SRC_IP} \
  --source-port-ranges '*' \
  --destination-address-prefixes ${DST_IP} \
  --destination-port-ranges 5306 \
  --access Allow --protocol ${PROTOCOL} \
  --description "description"