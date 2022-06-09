#!/bin/bash
#
# Query the DNS of the service once it is created.
#

DNS=$(aws cloudformation describe-stacks \
    --stack-name ECSWithALB \
    --query 'Stacks[*].Outputs[?OutputKey==`ExpenseLoggerALBDNS`].OutputValue' --output text
)
echo "DNS value: ${DNS}"