from fabric import operations as op

def run(aws):
    op.run('echo Installing git ...')
    op.run('sudo yum -y install git')
