from fabric import operations as op

def run(aws):
    # install Mysql
    op.run('echo Installing Mysql ...')
    op.run('sudo yum -y install mysql-server')

    # enable Mysql start on boot
    op.run('echo Enabling Mysql start on boot ...')
    op.run('sudo chkconfig mysqld on')

    # start Mysql
    op.run('echo Starting Mysql ...')
    op.run('sudo service mysqld start')

    # secure Mysql
    op.run('echo Securing Mysql ...')
    op.run('printf "\nY\n' + aws.options.mysql_root_pw + '\n' + aws.options.mysql_root_pw + '\nY\nY\nY\nY\n" | ' +
           'sudo /usr/bin/mysql_secure_installation')
