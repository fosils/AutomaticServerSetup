from __future__ import with_statement
from fabric import operations as op
from fabric import context_managers as cm
from fabric.contrib import files as cn

def run(aws):
    with cm.cd('~/'):
        cn.upload_template(aws.scripts_dir+'mysql.sh', '~/mysql.sh',context={'hostname':aws.reservation.public_dns_name},mirror_local_mode=True)
        op.run('sudo bash ./mysql.sh')
