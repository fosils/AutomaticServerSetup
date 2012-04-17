from __future__ import with_statement
from fabric import context_managers as cm
from fabric import operations as op

def run(aws):
    aws.run_task('install_mongodb')
    aws.run_task('install_php')
    aws.run_task('install_build_tools')

    # download MongoDB driver for PHP
    op.run('echo Downloading MongoDB driver for PHP ...')
    op.run('wget -O /tmp/mongo-.tgz -o /dev/null http://pecl.php.net/get/mongo')

    # install MongoDB driver for PHP (install_mongo_php.sh)
    op.run('echo Installing MongoDB driver for PHP ...')
    with cm.cd('/tmp'):
        op.run('tar xf mongo-.tgz')

    with cm.cd('/tmp/mongo-*'):
        op.run('phpize')
        op.run('./configure')
        op.run('make')
        op.run('sudo make install')

    op.run('echo -e "; Enable mongo extension module\nextension=mongo.so" | sudo tee /etc/php.d/mongo.ini')
    op.run('rm -rf /tmp/mongo-*')
