from fabric import operations as op

# command history to setup LamCMS on Amazon Linux AMI
def run(aws):
    aws.run_task('update_packages')

    ## this allows root to login with a hardcoded password, so don't run it by default
    # aws.run_task('sshd')

    aws.run_task('check_architecture')
    aws.run_task('setup_python')
    aws.run_task('install_git')
    aws.run_task('install_mongodb_for_php')
    aws.run_task('install_mysql')

    aws.run_task('lampcms_nodeps')

    aws.run_task('restart_apache')
