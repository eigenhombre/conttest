#!/usr/bin/env python
"""
Continuous Testing Helper

Usage:
  conttest <cmd> ...

"""

import hashlib
import os.path
import re
import subprocess
import sys
import time

HASHES = "hashes"
TIMES = "times"


def include_file_in_checks(path, excludes):
    """
    Determine whether file should be included in checks; reject if
    file has an undesired prefix, an undesired file extension, or
    lives in an undesired directory.
    """
    IGNORE_PREFIXES = ('.', '#')
    IGNORE_EXTENSIONS = ('pyc', 'pyo', '_flymake.py')
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
    return not excluded_pattern(path, excludes)


def excluded_pattern(root, excludes):
    for pat in excludes:
        if re.search(pat, root):
            return True



def getstate(full_path, method):
    if method == HASHES:
        try:
            content = open(full_path).read()
        except IOError:
            return None  # will trigger our action
        return hashlib.sha224(content).hexdigest()
    assert method == TIMES
    try:
        return os.path.getmtime(full_path)
    except OSError:  # e.g., broken link
        return None


def walk(top, method, filestates={}, excludes=[]):
    """
    Walk directory recursively, storing a hash value for any
    non-excluded file; return a dictionary for all such files.
    """
    for root, _, files in os.walk(top, topdown=False):
        for name in files:
            if excluded_pattern(name, excludes):
                continue
            full_path = os.path.join(root, name)
            if include_file_in_checks(full_path, excludes):
                filestates[full_path] = getstate(full_path, method)
    return filestates


def get_exclude_patterns_from_file(path):
    if not os.path.exists(path):
        return []
    with file(path) as f:
        return [s.strip() for s in f.read().split()
                if s.strip() != ""]


def show_diffs(a, b):
    """
    For debugging: print relevant diffs.
    """
    if abs((len(a.keys()) - len(b.keys()))) > 100:
        print("Massive change of keys:", len(a.keys()), "->", len(b.keys()))
    elif a.keys() != b.keys():
        print(set(a.keys()) - set(b.keys()))
    else:
        print([(k, a[k], b[k]) for k in a.keys() if a[k] != b[k]])


def watch_dir(dir_, callback, method=HASHES):
    """
    Loop continuously, calling function <callback> if any non-excluded
    file has changed.
    """
    filedict = {}
    while True:
        excludes = get_exclude_patterns_from_file(dir_ + "/.conttest-excludes")
        new = walk(dir_, method, {}, excludes=excludes)
        if new != filedict:
            callback()
            # Do it again, in case command changed files (don't retrigger)
            filedict = walk(dir_, method, {}, excludes=excludes)
        time.sleep(0.3)


def do_command_on_update(cmd):
    try:
        watch_dir(".", lambda: subprocess.call(cmd, shell=True),
                  method=TIMES)
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
