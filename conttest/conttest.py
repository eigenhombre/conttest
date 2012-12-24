#!/usr/bin/env python

"""
Continuous Testing Helper

Usage:
  conttest <cmd> ...

"""

import docopt
import time
import os.path
import sys
import hashlib
import subprocess


def include_file_in_checks(path):
    """
    Determine whether file should be included in checks; reject if
    file has an undesired prefix, an undesired file extension, or
    lives in an undesired directory.
    """
    IGNORE_PREFIXES = ('.', '#')
    IGNORE_EXTENSIONS = ('pyc', 'pyo')
    IGNORE_DIRS = ('.git', '.hg', '.svn')

    basename = os.path.basename(path)
    for p in IGNORE_PREFIXES:
        if basename.startswith(p):
            return False
    for extension in IGNORE_EXTENSIONS:
        if path.endswith(extension):
            return False
    parts = path.split(os.path.sep)
    for part in parts:
        if part in IGNORE_DIRS:
            return False
    return True


def skip_excludes(root, excludes):
    if root.startswith("./"):
        root = root[2:]
    return root.split('/')[0] in excludes


def walk(top, filehashes={}, excludes=[]):
    """
    Walk directory recursively, storing a hash value for any
    non-excluded file; return a dictionary for all such files.
    """
    for root, _, files in os.walk(top, topdown=False):
        if skip_excludes(root, excludes):
            continue
        for name in files:
            full_path = os.path.join(root, name)
            if include_file_in_checks(full_path):
                try:
                    content = open(full_path).read()
                except IOError:
                    continue
                hashcode = hashlib.sha224(content).hexdigest()
                filehashes[full_path] = hashcode
    return filehashes


def get_excludes(path):
    with file(path) as f:
        return [s.strip() for s in f.read().split()
                if s.strip() != ""]


def watch_dir(dir_, callback):
    """
    Loop continuously, calling function <callback> if any non-excluded
    file has changed.
    """
    filedict = {}
    while True:
        excludes = get_excludes(dir_ + "/.conttest-excludes")
        new = walk(dir_, {}, excludes=excludes)
        if new != filedict:
            callback()
            # Do it again, in case command changed files (don't retrigger)
            filedict = walk(dir_, {}, excludes=excludes)
        time.sleep(0.3)


def do_command_on_update(cmd):
    try:
        watch_dir(".", lambda: subprocess.call(cmd, shell=True))
    except KeyboardInterrupt:
        print


def main():
    cmd = ' '.join(sys.argv[1:])
    if cmd:
        do_command_on_update(cmd)
    else:
        print("Usage: %s command args ..." % __file__)


if __name__ == '__main__':
    main()
