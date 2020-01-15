<p align="center">
  <img src="./logo.png" alt="kar">
</p>

कर (/kəɾ/) is the hindi word for "do".

`kar` is a task runner with a simple goal in mind: make it dead simple to **wrap existing CLI tools**.

Most task runners focus on allowing you to specify task dependencies, running things in parallel, passing in multiple tasks at the same time, etc. `kar` does none of that.

`kar` focuses on **full argument propagation** to allow easily wrapping existing CLI tools. If you need to wrap an existing cli tool to make it easy to run daily tasks, preconfigured with your project-specific settings while still keeping the flexibility of passing arbitray arguments to the original tool, `kar` is for you.

**⚠This is alpha software, subject to change.⚠**

#### Common Use Cases

- wrap your custom `awslogs get` command with a preconfigured log group
- wrap your custom `docker run` command with preconfigured volumes and port mounts
- wrap your custom `jupyter lab` command with preconfigured host/ports/browser
- wrap your custom `ecs-cli up` command with preconfigured ecs cluster name and aws profile with the flexibility to change instance type or cluster size, i.e. `kar up --size 3 --instance-type t3.xlarge`
- any tool with a slightly annoying, hard to remember interface. anything in the awscli usually takes the 🍰

#### Installation

On macOS (or Linux with [Linuxbrew](https://docs.brew.sh/Homebrew-on-Linux)):

```
brew install AlJohri/-/kar
```

On Linux:

```
wget -P /usr/local/bin https://raw.githubusercontent.com/AlJohri/kar/master/kar
wget -P /usr/local/bin https://raw.githubusercontent.com/AlJohri/kar/master/help.sh
```

_The linux install will be improved later into a snap package or installer script._

#### Usage

Create a `Karfile`. Currently Bash and Python are supported:

<details>
	<summary>Bash</summary>

Any function starting with `task-` is a task. Annotate your tasks with the comments as shown below to get a nice interface when you run `kar help`.

```bash
#!/usr/bin/env bash

PROJECT=this-is-my-unique-project-name
AWS_PROFILE=mycompany

#@run
#+Run command in docker container.
task-run() {
    docker run -v "$(pwd)" -e AWS_PROFILE=$AWS_PROFILE $@
}

#@logs
#+Get logs from AWs Cloudwatch.
task-logs() {
    awslogs get /aws/lambda/$PROJECT --no-group $@
}

#@lab
#+Open Jupter Lab
task-lab() {
    docker run -v "$(pwd)" -e AWS_PROFILE=$AWS_PROFILE \
        python -m jupyter lab \
            --NotebookApp.token='' --ip=0.0.0.0 --port 8888 \
            --allow-root --no-browser 1>/dev/null $@
}
```

</details>

<details>
	<summary>Python</summary>

Any function starting with `task_` is a task. Annotate your tasks with the docstrings as shown below to get a nice interface when you run `kar help`.

```python
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
```

</details>

Then, you can run the tasks like:

```
$ kar help
run                      Run command in docker container.
lab                      Open Jupter Lab
logs                     Get logs from AWs Cloudwatch.
```

```
$ kar run
$ kar run python scripts/test.py
$ kar logs --timestamp -s "24hr"
$ kar lab notebooks/analysis.ipynb
```

#### Why not use Make/Rake/Invoke/Runner/etc.?

[Make](https://www.gnu.org/software/make/) syntax **sucks**! It's more annoying and difficult than it's often worth it to write simple tasks in Make. Make doesn't allow easily passing in arguments. You just can't do `make run python scripts/test.py`.

[Rake](https://github.com/ruby/rake) argument syntax is weird and it flat out doesn't allow just passing arbitary (hyphenated) arguments to existing cli commands.

[Invoke](https://github.com/pyinvoke/invoke/) gets much closer but it allows running multiple tasks in a single invocation which [doesn't make passing arbitrary arguments possible](https://github.com/pyinvoke/invoke/issues/693).

[Runner](https://github.com/stylemistake/runner) gets pretty close but it also allows running multiple tasks in a single invocation which is [incongruent with passing arbitrary arguments](https://github.com/stylemistake/runner/issues/37).

<!--
[NPM Scripts](https://docs.npmjs.com/misc/scripts) requries node and ...
[Gulp](https://gulpjs.com/) requires node and ...
[Grunt](https://gruntjs.com/) requires node and ...
-->

#### Credits

- This project uses `help-sh` for bash docstrings: https://github.com/dhamidi/help-sh
