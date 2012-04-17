from fabric import operations as op

def run(aws):
    op.run('echo Installing Apache ...')
    op.run('sudo yum -y install httpd')

    op.run('echo Enabling Apache start on boot ...')
    op.run('sudo chkconfig httpd on')

    op.run('echo Starting Apache ...')
    op.run('sudo service httpd start')
