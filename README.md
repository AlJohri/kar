<p align="center">
  <img src="./logo.png" alt="kar">
</p>

कर (/kəɾ/) is the hindi word for the "do".

`kar` is a task runner with a simple goal in mind: make it dead simple to **wrap existing CLI tools**.

Most task runners focus on allowing you to specify task dependencies, running thing in parallel, passing in multiple tasks at the same time, etc. `kar` does none of that.

`kar` focuses on **full argument propagation** to allow easily wrapping existing CLI tools. If you need to wrap an existing cli tool to make it easy to run daily tasks, preconfigured with your project-specific settings, while still keeping flexibility of passing arbitray arguments to the original tool, `kar` is for you.

#### Common Use Cases

- wrap your custom `awslogs get` command with the preconfigured log group for your project: `kar logs`
- wrap your custom `docker run` command with preconfigured volumes and port mounts yet still be able to pass arbitrary commands to the docker container: `kar run python scripts/pipeline.py`
- wrap your custom `jupyter lab` command with preconfigured host/ports and opening of the web browser of your choice: `kar lab`
- wrap your custom `ecs-cli up` command with preconfigured ecs cluster and aws profile yet still allowing you to change parameters: `kar up --size 3 --instance-type t3.xlarge`

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

Create a `Karfile`:

```bash
#!/bin/bash

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

#### Credit

- This repository uses `help-sh` for bash docstrings: https://github.com/dhamidi/help-sh
