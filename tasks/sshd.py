from fabric import operations as op
from fabric import context_managers as cm

def run(aws):
    # set temporary root password to pleasechangethispassword912
    op.run("echo '" + aws.options.aws_root_pw + "' | sudo passwd --stdin root")

    # install modified sshd_config
    with cm.cd('~/'):
        op.run("wget -o/dev/null https://abucketineurope.s3.amazonaws.com/sshd_config")
        op.run("sudo mv -f sshd_config /etc/ssh/")

    # restart sshd - if we don't sleep after doing this, sshd ends up dead for some reason I don't really understand
    op.run("sudo service sshd restart; sleep 1")
