from fabric import operations as op

def run(aws):
    # configure Yum repository to install MongoDB
    op.run('echo Configuring MongoDB repository Yum ...')
    op.run('echo [10gen] | sudo tee /etc/yum.repos.d/10gen.repo')
    op.run('echo name=10gen Repository | sudo tee -a /etc/yum.repos.d/10gen.repo')
    op.run('echo baseurl=http://downloads-distro.mongodb.org/repo/redhat/os/`arch` | sudo tee -a /etc/yum.repos.d/10gen.repo')
    op.run('echo gpgcheck=0 | sudo tee -a /etc/yum.repos.d/10gen.repo')

    # install MongoDB
    op.run('sleep 2')
    op.run('echo Installing MongoDB ...')
    op.run('sudo yum -y install mongo-10gen-server')

    # enable MongoDB start on boot
    op.run('echo Enabling MongoDB start on boot ...')
    op.run('sudo chkconfig mongod on')

    # start MongoDB
    op.run('echo Starting MongoDB ...')
    op.run('sudo service mongod start')
