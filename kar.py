#!/usr/local/bin/python3

import os
import sys
import inspect
import textwrap
import importlib
import importlib.util

KARFILE = os.getenv("KARFILE", "Karfile")


def load_karfile(path):
    importlib.machinery.SOURCE_SUFFIXES.append("")
    spec = importlib.util.spec_from_file_location("karfile", path)
    karfile = importlib.util.module_from_spec(spec)
    inject_globals(karfile)
    spec.loader.exec_module(karfile)
    return karfile


def inject_globals(module):

    import shlex
    import textwrap
    import argparse
    import functools
    from subprocess import run

    module.shlex = shlex
    module.argparse = argparse
    module.textwrap = textwrap
    module.functools = functools
    module.run = functools.partial(run, shell=True)

    def argument(*names_or_flags, **kwargs):
        return names_or_flags, kwargs

    def parse(*subparser_args, name=None, **parser_kwargs):
        def wrap(func):
            @functools.wraps(func)
            def decorator(argument_string):
                parser = argparse.ArgumentParser(
                    name or func.__name__.replace('task_', ''),
                    description=textwrap.dedent(str(func.__doc__)),
                    **parser_kwargs,
                )
                for args, kwargs in subparser_args:
                    parser.add_argument(*args, **kwargs)
                args = parser.parse_args(shlex.split(argument_string))
                return func(args)

            return decorator

        return wrap

    module.argument = argument
    module.parse = parse


def help(tasks, name=None):

    if name:
        task = tasks[cmd]
        print("{0:25}{1}".format(name, textwrap.dedent(str(task.__doc__)).strip(),))
    else:
        for name, task in tasks.items():
            print("{0:25}{1}".format(name, textwrap.dedent(str(task.__doc__)).strip(),))


if __name__ == "__main__":

    karfile = load_karfile(KARFILE)

    tasks = {
        fn.__name__.replace("task_", ""): fn
        for name, fn in inspect.getmembers(karfile, inspect.isfunction)
        if fn.__name__.startswith("task_")
    }

    sys.argv.pop(0)
    if len(sys.argv) == 0:
        print("Tasks:")
        help(tasks)
        exit(0)

    cmd = sys.argv.pop(0)

    if cmd not in tasks:
        print(f"Task {cmd} not found.")

    task = tasks[cmd]
    argspec = inspect.getfullargspec(task)
    if len(argspec.args) == 1 or argspec.varargs is not None:
        task(" ".join(sys.argv))
    else:
        task()
