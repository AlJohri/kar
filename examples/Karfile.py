#!/usr/bin/env python

# Example Passing in Raw Arguments
def task_foo(raw):
	run(f"echo {raw}")


# Example Parsing Arguments
@command(
	argument("instance_name", help="EC2 instance name")
)
def task_tag(args):
    print(args.instance_name)
