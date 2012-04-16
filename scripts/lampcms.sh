#!/bin/bash
# command history to setup LamCMS on Amazon Linux AMI

# variables used to define passwords and other parameters
# username and password to connect LampCMS database
MYSQL_LAMP_USER=root
MYSQL_LAMP_PW=root_pwd
# LampCMS administrator email
ADMIN_EMAIL=root@lampcms.net
# server URL without http://
SITE_HOST_NAME=%(hostname)s


# create LampCMS database in Mysql
echo Creating LampCMS database ...
mysql -u root mysql --password=$MYSQL_ROOT_PW <<EOF
create database LAMPCMS;
create user $MYSQL_LAMP_USER identified by '$MYSQL_LAMP_PW';
grant all privileges on LAMPCMS.* to $MYSQL_LAMP_USER with grant option;
quit
EOF

# configure Yum repository to install MongoDB
echo Configuring MongoDB repository Yum ...
echo [10gen] >> /etc/yum.repos.d/10gen.repo
echo name=10gen Repository >> /etc/yum.repos.d/10gen.repo
echo baseurl=http://downloads-distro.mongodb.org/repo/redhat/os/i686 >> /etc/yum.repos.d/10gen.repo
echo gpgcheck=0 >> /etc/yum.repos.d/10gen.repo


# install MongoDB
sleep 2
echo Installing MongoDB ...
yum -y install mongo-10gen-server
##Complete!


# enable MongoDB start on boot
echo Enabling MongoDB start on boot ...
chkconfig mongod on


# start MongoDB
echo Starting MongoDB ...
service mongod start
##Starting mongod:                                           [  OK  ]


#install pecl extension mongoDB
pecl install mongo


# download LampCMS package
cd /var/www
echo Downloading LampCMS package ...
wget -qO - https://github.com/fosils/LampCMS-for-Open-org.com/tarball/master | tar -xz

# install LampCMS (install_lampcms.sh)
echo Installing LampCMS
mv -f fosils-LampCMS-*/* ./
rmdir fosils-LampCMS-*
rm -rf html
mv www html
ln -s html www
if test ! -d /var/www/www/w/img/tmp/
then
mkdir /var/www/html/w/img/tmp
fi
chown -R apache /var/www/www/w
mkdir /var/log/php
chown apache /var/log/php


# configure LampCMS (config_lampcms.sh)
echo Configuring LampCMS ...
cd /var/www

mv -f \!config.ini.dist \!config.ini
mv -f acl.ini.dist acl.ini
mv -f Points.php.dist Points.php
mv -f Mycollections.php.dist Mycollections.php

cat \!config.ini | \
	sed "s/TCP_Port_number=/TCP_Port_number=3306/" | \
	sed "s/Database_username=/Database_username=$MYSQL_LAMP_USER/" | \
	sed "s/Database_password=/Database_password=$MYSQL_LAMP_PW/" | \
	sed "s/DEBUG = true/DEBUG = false/" | \
	sed "s/EMAIL_ADMIN = \"me@me.me\"/EMAIL_ADMIN= \"$ADMIN_EMAIL\"/" | \
	sed "s/EMAIL_DEVELOPER = \"me@me.me\"/EMAIL_DEVELOPER = \"$ADMIN_EMAIL\"/" | \
	sed "s/SITE_URL=\"http:\/\/localhost\"/SITE_URL=\"http:\/\/$SITE_HOST_NAME\"/" | \
	sed "s/LOG_FILE_PATH = php.log/LOG_FILE_PATH = \/var\/log\/php\/php.log/" | \
	sed "s/LOG_FILE_PATH_CGI = cgiphp.log/LOG_FILE_PATH_CGI = \/var\/log\/php\/cgiphp.log/" | \
	sed "s/LAMPCMS_PATH =\"\/\"/LAMPCMS_PATH =\"\/var\/www\"/" | \
	sed "s/LAMPCMS_DATA_DIR =/LAMPCMS_DATA_DIR =\"\/var\/www\/html\/w\"/" | \
	sed "s/CATEGORIES = 2/CATEGORIES = 1/" | \
	sed "s/;twitter/twitter/" | \
	sed "s/;facebook/facebook/" | \
	sed "s/;linkedin/linkedin/" > config.new
mv -f config.new \!config.ini
sed "s/# RewriteEngine on/RewriteEngine on/" RewriteRules.txt > /etc/httpd/conf.d/lampcms.conf

# restart Apache
echo Restarting Apache ...
service httpd restart#
##Starting httpd:                                            [  OK  ]
