#!/bin/bash -e

trap cleanup ERR

function cleanup {
  echo "Cleaning up!"
  kubectl delete ns/dynamodb
}

case $1 in
  "on")
    kubectl create ns dynamodb
    kubectl apply -f templates/dynamodb.yaml
    kubectl wait --all --for=condition=Ready -l app=dynamodb pod -n dynamodb --timeout=60s
    kubectl apply -f templates/create-table.yaml
    kubectl wait --all --for=condition=Complete=True job -n dynamodb --timeout=60s
    ;;
  "off")
    cleanup
    ;;
  *)
    echo "[ERR] Accept only: deploy-dynamodb on|off"
    ;;
esac
