from __future__ import with_statement
from fabric import operations as op

def run(aws):
    op.run('sudo yum update -y')
