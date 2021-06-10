#!/usr/bin/env bash
set -e

apt-get install jq -y

aws sts get-caller-identity

pip install -r requirements_dev.txt -r requirements.txt --cache-dir=/root/cache/pip
npm config set cache=/root/cache/npm
npm install -g aws-cdk
