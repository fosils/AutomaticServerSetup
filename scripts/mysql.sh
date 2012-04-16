#!/bin/bash

# Mysql root password
MYSQL_ROOT_PW=root


# install Mysql
echo Installing Mysql ...
yum -y install mysql-server
##Complete!


# enable Mysql start on boot
echo Enabling Mysql start on boot ...
chkconfig mysqld on


# start Mysql
echo Starting Mysql ...
service mysqld start
##Starting mysqld:                                           [  OK  ]

# secure Mysql
echo Securing Mysql ...
/usr/bin/mysql_secure_installation <<EOF
COMMANDS

Y
$MYSQL_ROOT_PW
$MYSQL_ROOT_PW
Y
Y
Y
Y
COMMANDS
EOF

