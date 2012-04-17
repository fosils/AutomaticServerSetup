#!/bin/bash

# set temporary root password to pleasechangethispassword912
echo pleasechangethispassword912 | passwd --stdin root
wget https://abucketineurope.s3.amazonaws.com/sshd_config
mv -f sshd_config /etc/ssh/
/etc/init.d/sshd restart
sleep 1
