from fabric import operations as op

def run(aws):
    aws.run_task('install_apache')

    op.run('echo Installing PHP and modules ...')
    op.run('sudo yum -y install php php-devel php-mbstring php-pecl-apc php-pecl-oauth php-gd php-xml re2c')
    op.run('sudo pecl channel-update pecl.php.net')
