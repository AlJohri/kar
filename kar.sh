#!/usr/local/bin/bash

source $(dirname $(realpath "$0"))/help.sh

KARFILE=${KARFILE:-Karfile}
source $KARFILE

tasks=$(declare -F | cut -d' ' -f3 | grep "task-" | \
	awk '{gsub("task-",""); print}')

if [ $# -eq 0 ]; then
    echo "Tasks:"
	help $KARFILE
    exit 0
fi

cmd="$1"
shift 1

for task in $tasks; do
	if [ "$cmd" = "$task" ]; then
		task-$cmd $@
		exit 0
	fi
done

if [ "$cmd" = "help" ]; then
	help $KARFILE
	exit 0
fi

echo "Task $cmd" not found.
exit 1
