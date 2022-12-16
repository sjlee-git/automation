## Variables
EC2_ROLE="EC2_ROLE_NAME"
LB_NAME=""

## Main

echo " Deregistering ${LB_NAME}'s Target ..."

CLB_LIST=$(aws elb describe-load-balancers --query LoadBalancerDescriptions[*].LoadBalancerName --output text | sed -E 's/\s+/\n/g' --profile ${EC2_ROLE})
ALB_LIST=$(aws elbv2 describe-load-balancers --query 'LoadBalancers[*].LoadBalancerName' --output text | sed -E 's/\s+/\n/g' --profile ${EC2_ROLE})

if [[ "${CLB_LIST}" =~ "${LB_NAME}" ]]; then
  echo " CLB"
  # Get Instance Id
  CLB_TAGET_ID=$(aws elb describe-load-balancers --load-balancer-name "${LB_NAME}" --query 'LoadBalancerDescriptions[].Instances[].[InstanceId]' --output text --profile ${EC2_ROLE})
  # Deregister Target
  aws elb deregister-instances-from-load-balancer --load-balancer-name "${LB_NAME}" --instances ${CLB_TAGET_ID} --profile ${EC2_ROLE}
  sleep 5
  # CLB Target Check
  if [[ -z "${CLB_TAGET_ID}" ]]; then
    echo " Successfully detached"
  else
    echo " Instance still exists"
  fi


elif [[ "${ALB_LIST}" =~ "${LB_NAME}" ]]; then
  echo " ALB"
  # Get ALB ARN
  ALB_ARN=$(aws elbv2 describe-load-balancers --names "${LB_NAME}" --query 'LoadBalancers[*].LoadBalancerArn' --output text --profile ${EC2_ROLE})
  # Get TargetGroup ARN
  TG_ARN=$(aws elbv2 describe-target-groups --load-balancer-arn ${ALB_ARN} --query 'TargetGroups[].TargetGroupArn' --output text --profile ${EC2_ROLE})
  # Get Instance Id
  TG_INSTANCE_LIST=$(aws elbv2 describe-target-health --target-group-arn ${TG_ARN} --query 'TargetHealthDescriptions[].Target[].[Id]' --output text --profile ${EC2_ROLE})
  # Deregister Target
  for TARGET in ${TG_INSTANCE_LIST[@]}; do
    echo "${TARGET}"
    aws elbv2 deregister-targets \
    --target-group-arn ${TG_ARN} \
    --targets Id=${TARGET} --profile ${EC2_ROLE}
  done
  sleep 5
  # ALB Target Check
  if [[ -z "${TG_INSTANCE_LIST}" ]]; then
    echo " Successfully detached"
  else
    echo " Instance still exists"
  fi

else
  echo " There is no LB named ${LB_NAME}"
fi