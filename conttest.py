#!/usr/bin/env python

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


def walk(top, filehashes={}):
    """
    Walk directory recursively, storing a hash value for any
    non-excluded file; return a dictionary for all such files.
    """
    for root, _, files in os.walk(top, topdown=False):
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


def watch_dir(dir_, callback):
    """
    Loop continuously, calling function <callback> if any non-excluded
    file has changed.
    """
    filedict = {}
    while True:
        new = walk(dir_, {})
        if new != filedict:
            callback()
        filedict = new
        time.sleep(0.3)


def do_command_on_update(cmd):
    def on_update():
        subprocess.call(cmd, shell=True)
    try:
        watch_dir(".", on_update)
    except KeyboardInterrupt:
        print


if __name__ == "__main__":
    cmd = ' '.join(sys.argv[1:])
    if cmd:
        do_command_on_update(cmd)
    else:
        print("Usage: %s command args ..." % __file__)
