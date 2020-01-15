#!/usr/local/bin/python3

import sys
import importlib
import importlib.util

if len(sys.argv) == 1:
    print("insert help here...")
    exit(0)

sys.argv.pop(0)

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


    def command(*subparser_args, name=None, **parser_kwargs):
        def wrap(func):
            func.__dict__['parse'] = True
            @functools.wraps(func)
            def decorator(argument_string):
                parser = argparse.ArgumentParser(
                    name or func.__name__,
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
    module.command = command


importlib.machinery.SOURCE_SUFFIXES.append('')
spec = importlib.util.spec_from_file_location('karfile', 'Karfile')
karfile = importlib.util.module_from_spec(spec)
inject_globals(karfile)
spec.loader.exec_module(karfile)

cmd = sys.argv[0]
sys.argv.pop(0)

if f'task_{cmd}' not in dir(karfile):
    print(f"Task {cmd} not found.")

task = getattr(karfile, f'task_{cmd}')

import inspect
argspec = inspect.getfullargspec(task)

if len(argspec.args) == 1 or argspec.varargs is not None:
    task(' '.join(sys.argv))
else:
    task()
