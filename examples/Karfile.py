#!/usr/bin/env python

def task_run(raw):
    """
    Run command in docker container.
    """
    run(f"docker run -it busybox {raw}")


@parse(argument("instance_name", help="EC2 instance name"))
def task_ec2(args):
    """
    Blah blah blah
    """
    print(f"Starting EC2 instance {args.instance_name}")
