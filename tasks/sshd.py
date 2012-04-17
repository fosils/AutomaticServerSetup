from fabric import operations as op
from fabric import context_managers as cm

def run(aws):
    # set temporary root password to pleasechangethispassword912
    op.run("echo pleasechangethispassword912 | sudo passwd --stdin root")

    # install modified sshd_config
    with cm.cd('~/'):
        op.run("wget -o/dev/null https://abucketineurope.s3.amazonaws.com/sshd_config")
        op.run("sudo mv -f sshd_config /etc/ssh/")

    # restart sshd
    op.run("sudo service sshd restart; sleep 1")
