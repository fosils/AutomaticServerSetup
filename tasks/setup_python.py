from fabric import operations as op

def run(aws):
    op.run('sudo yum install python python-devel gcc -y')
    op.run('sudo easy_install pip')
    op.run('sudo pip install boto fabric')
