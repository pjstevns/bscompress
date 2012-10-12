#!/usr/bin/python

import os
import sys
import hashlib
import subprocess

DIR = "var/blobstorage"


def checkPath(path):
    if os.path.isdir(path):
        return
    checkPath(os.path.dirname(path))
    os.mkdir(path, 0700)


def getHashPath(hash):
    assert(len(hash) > 5)
    path = os.path.join(DIR, 'objects', hash[0], hash[1])
    checkPath(path)
    return os.path.join(path, hash)


def scanner(base):
    sys.stdout.write('scanning... ')
    sys.stdout.flush()
    for root, dirs, files in os.walk(base):
        files = [x for x in files if x.endswith('.blob')]
        for file in files:
            sys.stdout.write('.')
            oidpath = os.path.join(root, file)
            data = open(oidpath, 'r').read()
            hash = hashlib.sha1(data).hexdigest()
            hashpath = getHashPath(hash)
            if os.path.isfile(hashpath):
                if os.stat(oidpath).st_nlink == 1:
                    os.remove(oidpath)
                    os.link(hashpath, oidpath)
            else:
                os.link(oidpath, hashpath)
    sys.stdout.write('done\n')
    sys.stdout.flush()

if __name__ == '__main__':
    print "Current usage"
    subprocess.call(["du", "-ms", DIR])
    table = scanner(DIR)
    print "Optimized usage"
    subprocess.call(["du", "-ms", DIR])

#EOF
