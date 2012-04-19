from fabric import operations as op

def run(aws):
    aws.run_task('install_mysql')

    # install php-mysql
    op.run('sudo yum -y install php-mysql')
