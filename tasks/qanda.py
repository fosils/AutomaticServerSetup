from __future__ import with_statement
from fabric import context_managers as cm
from fabric import operations as op

# command history to setup QandA site on Amazon Linux AMI
def run(aws):
    aws.run_task('update_packages')

    ## this allows root to login with a hardcoded password, so don't run it by default
    # aws.run_task('sshd')

    aws.run_task('check_architecture')
    aws.run_task('setup_python')
    aws.run_task('install_apache')
    aws.run_task('install_php')
    aws.run_task('install_mysql')

    # download QandA package
    op.run('echo Downloading QandA package ...')
    with cm.cd('/var/www/html'):
        op.run('wget -qO - https://github.com/dkode/QA-website/tarball/master | sudo tar -xz')

        # install QA
        op.run('echo Installing QA-website')
        op.run('sudo mv -f dkode-QA-*/* ./')
        op.run('sudo rmdir dkode-QA-*')
