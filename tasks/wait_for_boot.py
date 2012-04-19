import time

from fabric import operations as op
from fabric.exceptions import NetworkError

def run(aws):
    print "Waiting for instance to boot..."
    while True:
        time.sleep(10)
        try:
            op.run('echo -n "ready?"')
            break
        except NetworkError:
            pass
    print "It's ready!"
