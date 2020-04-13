# aws-cli-manager
Command line tool to manager aws resources EC2

## About

This project works with AWS EC2 resources and uses boto3 to manage the resources. We have names this project as "bouncy"

## Configuration

Bouncy does uses the credentials ( access key & secret key id ) configured for aws cli. 
Need to create a functional user having full access to EC2 resource with programatic access ( access_key_id and secret_key_id )

How to configured AWS CLI profile:- 
* aws configure --profile bouncy
* aws_access_key_id = *********************************
* aws_secret_access_key = **********************************
* region = us-east-1 
* output = json


