from fabric import operations as op

def run(aws):
    # install GCC compiler and Make
    op.run('echo Installing GCC compiler and make ...')
    op.run('sudo yum -y install gcc make')
