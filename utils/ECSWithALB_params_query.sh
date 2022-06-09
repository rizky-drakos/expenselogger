#!/bin/bash
#
# Queries for VPCs, subnets and security groups that 
# are needed for the ECSWithALB.json template.  
#

VPCs=$(aws ec2 describe-vpcs --query 'Vpcs[*].VpcId' --output text)
echo "* Available VPCs: ${VPCs}"

for VPC in ${VPCs}; do
    echo "* Available subnets and security groups by ${VPCs}:"
    echo "- Subnets:"
    aws ec2 describe-subnets --query "Subnets[?VpcId==\`${VPCs}\`].SubnetId" --output table
    echo "- Security groups:"
    aws ec2 describe-security-groups --query "SecurityGroups[?VpcId==\`${VPCs}\`].GroupId" --output table
done
