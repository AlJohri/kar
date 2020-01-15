#!/usr/bin/env python

@task
def run(raw):
    """
    Run command in docker container.
    """
    shell(f"docker run -it ubuntu {raw}")

@task(split=True)
def ec2(instance_name, vpc_tag):
    """
    Run command in docker container.
    """
    print(f"Starting EC2 instance in {vpc_tag} VPC with name: {instance_name}")

@task(name='list')
def list_():
    """
    List files in current directory.
    """
    shell(f"ls -lha")
