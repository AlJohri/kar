#!/bin/bash

PROJECT=this-is-my-unique-project-name
AWS_PROFILE=mycompany

#@run
#+Run command in docker container.
task-run() {
    docker run -it -v "$(pwd)" -e AWS_PROFILE=$AWS_PROFILE busybox $@
}

#@logs
#+Get logs from AWs Cloudwatch.
task-logs() {
    awslogs get /aws/lambda/$PROJECT --no-group $@
}

#@lab
#+Open Jupter Lab
task-lab() {
    docker run -it -v "$(pwd)" -e AWS_PROFILE=$AWS_PROFILE busybox \
        python -m jupyter lab \
            --NotebookApp.token='' --ip=0.0.0.0 --port 8888 \
            --allow-root --no-browser 1>/dev/null $@
}
