#!/bin/bash

## Directory info
sdir="/var/log/<>"
sdirerr="/var/log/<>"
s3json="s3://<>"

## hostname
servername=`hostname -s`

## Date
today=`date '+%Y-%m-%d'`
yesterday=`date '+%Y-%m-%d' -d '-1days'`

## S3 Upload

# Game Log(exclude error/ directory)
aws s3 sync $sdir $s3json/$servername/$today --exclude "*" --include "*$today.log*" --exclude "*error*" --delete --acl bucket-owner-full-control
aws s3 sync $sdir $s3json/$servername/$yesterday --exclude "*" --include "*$yesterday.log*" --exclude "*error*" --delete --acl bucket-owner-full-control

# Error Log
aws s3 sync $sdirerr $s3json/$servername/$today --exclude "*" --include "*$today*.error.log*" --delete --acl bucket-owner-full-control
aws s3 sync $sdirerr $s3json/$servername/$yesterday --exclude "*" --include "*$yesterday*.error.log*" --delete --acl bucket-owner-full-control