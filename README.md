# kar

कर (/kəɾ/) is the hindi word for `do`. `kar` is a task runner with a simple goal in mind: make it dead simple to **wrap existing CLI tools**. Most task runners focus on allowing you to specify task dependencies, running things in parallel, running multiple tasks simultaneously, etc. `kar` does none of that. `kar` focuses on full argument propagation to allow easily wrapping existing CLI tools. If you need to wrap an existing cli tool to make easy to run daily tasks, preconfigured with your project specific settings, yet without losing the ability to pass in arbitrary arguments, `kar` is for you.

Example Use Cases:
	- wrap your custom `awslogs get` command with the preconfigured log group for your project: `kar logs`
	- wrap your custom `docker run` command with preconfigured volumes and port mounts yet still be able to pass arbitrary commands to the docker container: `kar run python scripts/pipeline.py`
	- wrap your custom `jupyter lab` command with preconfigured host/ports and opening of the web browser of your choice: `kar lab`
	- wrap your custom `ecs-cli up` command with preconfigured ecs cluster and aws profile yet still allowing you to change parameters: `kar up --size 3 --instance-type t3.xlarge`

Currently, `kar` allows you to specify tasks in `bash` as `bash` lends itself very well to argument propagation.

Installation:

```
brew install AlJohri/-/kar
```

Usage:

Create a `Karfile` (or `Karfile.sh`):

```bash
PROJECT=this-is-my-unique-project-name
AWS_PROFILE=mycompany

task-run() {
    docker run -v "$(pwd)" -e AWS_PROFILE=$AWS_PROFILE $@
}

task-logs() {
    awslogs get /aws/lambda/$PROJECT $@
}

task-lab() {
    docker run -v "$(pwd)" -e AWS_PROFILE=$AWS_PROFILE \
        python -m jupyter lab \
            --NotebookApp.token='' --ip=0.0.0.0 --port 8888 \
            --allow-root --no-browser 1>/dev/null $@
}
```

Then, you can run the tasks like:

```
$ kar run
```

```
$ kar logs
```
