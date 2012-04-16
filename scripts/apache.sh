#!/bin/bash

# install Apache
echo Installing Apache ...
yum -y install httpd
##Complete!

# enable Apache start on boot
echo Enabling Apache start on boot ...
chkconfig httpd on


# start Apache
echo Starting Apache ...
service httpd start
##Starting httpd:                                            [  OK  ]
