# aws-cli-manager
Command line tool to manage aws resources EC2

## About

This project works with AWS EC2 resources and uses boto3 to manage the resources. We have named this project as "bouncy"

## Configuration

Bouncy does uses the credentials ( access key & secret key id ) configured for aws cli. 
Need to create a functional user having full access to EC2 resource with programatic access ( access_key_id and secret_key_id )

How to configure AWS CLI profile:- 
* aws configure --profile bouncy
* aws_access_key_id = *********************************
* aws_secret_access_key = **********************************
* region = us-east-1 
* output = json

### Installation Requirents 
The code has been developed to adapt with python3 version. Below are the required packages for this project

* python virtual env
`pip3 install pipenv`
* Python3
`pipenv --three`
* Click
`pipenv install click`
* boto3
`pipenv install boto3`
* setuptools 
`pipenv install setuptools`

### Running the tool
* Go to virtual env shell
`pipenv shell`
* Run the command as follows
`python bouncy/bouncy.py --profile <profile_name> <command> <subcommand> --project <project_name>`
* Commands are instances, volumes, or snapshots 
* Subcommands depends on command project is optional

### Installing the module as package
* Creating a distribution package and installing the package using setup.py in egg format.
`pipenv install --editable .`
* This makes the tool running easy 
1.  Go to virtual env shell `pipenv shell`
2. Give the required using the tool name, <bouncy> here `bouncy --profile sandy instances --help`

"""(aws-cli-manager) bash-3.2$ bouncy --profile sandy instances --help
Usage: bouncy instances [OPTIONS] COMMAND [ARGS]...

  Commands for Instances

Options:
  --help  Show this message and exit.

Commands:
  list       Command to list the EC2 istances.
  snapshots  Command to create snapshot of the ec2 instances
  start      Command to start the ec2 instances
  stop       Command to stop the ec2 instances"""


* Creating a distribution package in wheel format
1. Go to virtual env shell `pipenv shell`
2. Create the distribution package `python setup.py bdist_wheel`
3. A `dist` folder should be created in the current directory having `*.whl` package (eg:- bouncy-0.1-py3-none-any.whl)



