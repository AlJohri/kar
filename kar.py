#!/usr/local/bin/python3

import os
import sys
import shlex
import inspect
import argparse
import textwrap
import functools
import subprocess
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


def run_variadic(func, *args, **kwargs):
    argspec = inspect.getfullargspec(func)
    if len(argspec.args) == 0 and argspec.varargs is None:
        func()
    else:
        func(*args, **kwargs)

def cli_from_func(func):
    argspec = inspect.getfullargspec(func)
    parser = argparse.ArgumentParser(
        prog=func.__dict__["task"],
        description=textwrap.dedent(str(func.__doc__ or ''))
    )

    kwonlydefaults = argspec.kwonlydefaults or {}

    if argspec.varkw:
        raise NotImplementedError()

    for arg in argspec.args:
        parser.add_argument(arg, default=kwonlydefaults.get(arg))

    for arg in argspec.kwonlyargs:
        if kwonlydefaults[arg] == False:
            action = 'store_true'
        elif kwonlydefaults[arg] == True:
            action = 'store_false'
        else:
            action = 'store'
        parser.add_argument(f'--{arg}', action=action, default=kwonlydefaults[arg])

    if argspec.varargs:
        parser.add_argument(argspec.varargs, nargs='?')

    return parser

def inject_globals(module):

    module.shell = functools.partial(subprocess.run, shell=True)

    def task(func=None, *, name=None, split=False, parse=False):
        if func is None:
            return functools.partial(task, name=name, split=split, parse=parse)
        func.__dict__["task"] = name or func.__name__

        @functools.wraps(func)
        def decorator(*args, **kwargs):
            if parse:
                argument_string = args[0]
                parser = cli_from_func(func)
                args = parser.parse_args(shlex.split(argument_string))
                return func(**args.__dict__)
            elif split:
                argument_string = args[0]
                return func(*shlex.split(argument_string))
            else:
                run_variadic(func, *args, **kwargs)
        return decorator

    module.task = task

    # # don't expose full argument parsing yet
    # import argparse
    # def argument(*names_or_flags, **kwargs):
    #     return names_or_flags, kwargs
    # def parse(*subparser_args, name=None, **parser_kwargs):
    #     def wrap(func):
    #         @functools.wraps(func)
    #         def decorator(argument_string):
    #             parser = argparse.ArgumentParser(
    #                 name or func.__name__.replace("task_", ""),
    #                 description=textwrap.dedent(str(func.__doc__)),
    #                 **parser_kwargs,
    #             )
    #             for args, kwargs in subparser_args:
    #                 parser.add_argument(*args, **kwargs)
    #             args = parser.parse_args(shlex.split(argument_string))
    #             return func(args)

    #         return decorator

    #     return wrap
    # module.argument = argument
    # module.parse = parse


def help(tasks, name=None):

    if name:
        task = tasks[cmd]
        print(
            "{0:25}{1}".format(name, textwrap.dedent(str(task.__doc__ or "")).strip(),)
        )
    else:
        for name, task in tasks.items():
            print(
                "{0:25}{1}".format(
                    name, textwrap.dedent(str(task.__doc__ or "")).strip(),
                )
            )


if __name__ == "__main__":

    karfile = load_karfile(KARFILE)

    tasks = {
        fn.__dict__["task"]: fn
        for name, fn in inspect.getmembers(karfile, inspect.isfunction)
        if fn.__dict__.get("task")
    }

    sys.argv.pop(0)
    if len(sys.argv) == 0:
        print("Tasks:")
        help(tasks)
        exit(0)

    cmd = sys.argv.pop(0)

    if cmd not in tasks:
        print(f"Task {cmd} not found.")
        exit(1)

    task = tasks[cmd]
    run_variadic(task, " ".join(sys.argv))
