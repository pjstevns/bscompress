#!/usr/bin/python

import os
import sys
import hashlib
import subprocess

DIR = "var/blobstorage"


def scanner(base):
    HASH = {}
    sys.stdout.write('scanning... ')
    sys.stdout.flush()
    for root, dirs, files in os.walk(base):
        files = [x for x in files if x.endswith('.blob')]
        for file in files:
            filepath = os.path.join(root, file)
            data = open(filepath, 'r').read()
            hash = hashlib.sha1(data).hexdigest()
            if hash not in HASH:
                HASH[hash] = []
            HASH[hash].append(filepath)
    sys.stdout.write('done\n')
    sys.stdout.flush()
    return HASH


def optimizer(table):
    sys.stdout.write('optimizing... ')
    sys.stdout.flush()
    for files in table.values():
        master, slaves = files[0], files[1:]
        if not slaves:
            continue
        if os.stat(master).st_nlink == len(files):
            continue
        for slave in slaves:
            os.unlink(slave)
            os.link(master, slave)
    sys.stdout.write('done\n')
    sys.stdout.flush()


if __name__ == '__main__':
    print "Current usage"
    subprocess.call(["du", "-ms", DIR])
    table = scanner(DIR)
    optimizer(table)
    print "Optimized usage"
    subprocess.call(["du", "-ms", DIR])

#EOF
