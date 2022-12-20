#!/bin/bash

# VARIABLES
SUBSCRIPTION="subscription"
GROUP=<resource_group>
REGION=<region>
VNET=<virtual_network>
SUBNET=<subnet>
# VM_SIZE=Standard_D4s_v3 # (4 vCPU 16 GiB)
# VM_SIZE=Standard_F2s_v2 # (2 vCPU 4 GiB)
VM_SIZE=Standard_F4s_v2 # (4 vCPU 8 GiB)
# VM_SIZE=Standard_F8s_v2 # (4 vCPU 8 GiB)
# VM_SIZE=Standard_F16s_v2 # (16 vCPU 32 GiB)
USERNAME=<username>
PASSWORD="<password>"
BOOTDIAG=<diagnostics>
PREFIX=<prefix>


# COMMON
az account set -s "subscription"
az configure --defaults group=${GROUP}
az configure --defaults location=${REGION}


# NIC
az network nic create -g ${GROUP} -n naming_nic \
  --vnet-name ${VNET} --subnet ${SUBNET} \
  --private-ip-address 0.0.0.0


# IP CONFIG
az network nic ip-config update -g ${GROUP} -n naming_ipconfig \
  --nic-name ${PREFIX}-nic


# OS DISK
az disk create -g ${GROUP} -n ${PREFIX}-os -l ${REGION} \
  --gallery-image-reference-lun /subscriptions/<subscription>/resourceGroups/<resource_group>/providers/Microsoft.Compute/galleries/<compute_gallery>/images/<images>/versions/0.0.1 \
  --size-gb 128 --hyper-v-generation V2

az disk create -g <resource_group> -n naming_disk \
  --gallery-image-reference /subscriptions/<subscription>/resourceGroups/<resource_group>/providers/Microsoft.Compute/galleries/<compute_gallery>/images/<images>/versions/0.0.1 \
  --size-gb 128 --hyper-v-generation V2

# DATA DISK
STORAGE_TYPE=Premium_LRS

az disk create -g ${GROUP} -n naming_disk -l ${REGION} \
  --sku ${STORAGE_TYPE} --size-gb 256 --hyper-v-generation V2
