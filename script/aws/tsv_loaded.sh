#!/bin/sh

## Directory info
# sdir="/var/log/<>"
sdir="/root"
s3="s3://<>"

## Date
LOG_DIR=$(ls ${sdir}/*.sh)
# past_date=$(ls ${sdir} | cut -d '_' -f1)

## S3 Upload
# aws s3 sync ${sdir} ${s3}/${past_date} --exclude "*" --include "*${past_date}*.tsv" --acl bucket-owner-full-control

for FILE in ${LOG_DIR[@]}; do

  ORG_DATE=$(date +"%Y%m%d" -r ${FILE})
  ORG_HOUR=$(date +"%H" -r ${FILE})
  ORG_MINU=$(date +"%M" -r ${FILE})

  UTC_DATE=$(date -d "${ORG_DATE} -9 hour" +"%Y%m%d")

  if [[ ${ORG_HOUR#0} -eq "0" ]] && [[ ${ORG_MINU#0} -lt "10" ]]; then
    # 15:00~15:05 KST => UTC YESTERDAY
    S3_DATE=$(date -d "${UTC_DATE} -1 day" +"%Y%m%d")

    echo "${FILE}"
    echo " HOUR : ${ORG_HOUR#0}"
    echo " MINUTES ${ORG_MINU#0}"
    echo " KST Date : ${ORG_DATE}"
    echo " UTC Date : ${UTC_DATE}"
    echo "  S3 Date : ${S3_DATE}"
    # aws s3 sync ${sdir} ${s3}/${S3_DATE} --exclude "*" --include "${FILE}" --acl bucket-owner-full-control
    echo " UTC YESTERDAY Upload"
    echo ""
  else
    echo "${FILE}"
    echo " HOUR : ${ORG_HOUR#0}"
    echo " MINUTES ${ORG_MINU#0}"
    echo " KST Date : ${ORG_DATE}"
    echo " UTC Date : ${UTC_DATE}"
    # aws s3 sync ${sdir} ${s3}/${UTC_DATE} --exclude "*" --include "${FILE}" --acl bucket-owner-full-control
    echo " UTC Upload"
    echo ""
  fi

done
