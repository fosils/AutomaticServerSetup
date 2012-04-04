# command history to setup LamCMS on Amazon Linux AMI

# set temporary root password to pleasechangethispassword912
echo pleasechangethispassword912 | passwd --stdin root
wget https://abucketineurope.s3.amazonaws.com/sshd_config
mv -f sshd_config /etc/ssh/
/etc/init.d/sshd restart


# variables used to define passwords and other parameters
# Mysql root password
MYSQL_ROOT_PW=root
# username and password to connect LampCMS database
MYSQL_LAMP_USER=root
MYSQL_LAMP_PW=root_pwd
# LampCMS administrator email
ADMIN_EMAIL=root@lampcms.net
# server URL without http://
SITE_HOST_NAME=%(hostname)s

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


# install PHP
echo Installing PHP and modules ...
yum -y install php php-devel php-mbstring php-pecl-apc php-pecl-oauth php-gd php-xml re2c
##Complete!


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


# install GCC compiler and Make
echo Installing GCC compiler ...
yum -y install gcc make
##Complete!


# download MongoDB driver for PHP
echo Downloading MongoDB driver for PHP ...
wget -O /tmp/mongo-.tgz -o /dev/null http://pecl.php.net/get/mongo


# install MongoDB driver for PHP (install_mongo_php.sh)
echo Installing MongoDB driver for PHP ...
cd /tmp
tar xf mongo-.tgz
cd /tmp/mongo-*
phpize
./configure
make
make install
echo -e "; Enable mongo extension module\nextension=mongo.so" > /etc/php.d/mongo.ini
cd /tmp
rm -rf /tmp/mongo-*


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

# create LampCMS database in Mysql
echo Creating LampCMS database ...
mysql -u root mysql --password=$MYSQL_ROOT_PW <<EOF
create database LAMPCMS;
create user $MYSQL_LAMP_USER identified by '$MYSQL_LAMP_PW';
grant all privileges on LAMPCMS.* to $MYSQL_LAMP_USER with grant option;
quit
EOF

# download LampCMS package
echo Downloading LampCMS package ...
wget -O /tmp/lampcms.zip -o /dev/null https://github.com/snytkine/LampCMS/zipball/master


# install LampCMS (install_lampcms.sh)
echo Installing LampCMS ...
cd /tmp
unzip lampcms.zip > /dev/null
rm lampcms.zip
cp -Rf snytkine-LampCMS-*/* /var/www
rm -rf snytkine-LampCMS-*
cd /var/www
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

sed "s/TCP_Port_number=/TCP_Port_number=3306/" \!config.ini > config.new
mv -f config.new \!config.ini
sed "s/Database_username=/Database_username=$MYSQL_LAMP_USER/" \!config.ini > config.new
mv -f config.new \!config.ini
sed "s/Database_password=/Database_password=$MYSQL_LAMP_PW/" \!config.ini > config.new
mv -f config.new \!config.ini
sed "s/DEBUG = true/DEBUG = false/" \!config.ini > config.new
mv -f config.new \!config.ini
sed "s/EMAIL_ADMIN = \"me@me.me\"/EMAIL_ADMIN= \"$ADMIN_EMAIL\"/" \!config.ini > config.new
mv -f config.new \!config.ini
sed "s/EMAIL_DEVELOPER = \"me@me.me\"/EMAIL_DEVELOPER = \"$ADMIN_EMAIL\"/" \!config.ini > config.new
mv -f config.new \!config.ini
sed "s/SITE_URL=\"http:\/\/localhost\"/SITE_URL=\"http:\/\/$SITE_HOST_NAME\"/" \!config.ini > config.new
mv -f config.new \!config.ini
sed "s/LOG_FILE_PATH = php.log/LOG_FILE_PATH = \/var\/log\/php\/php.log/" \!config.ini > config.new
mv -f config.new \!config.ini
sed "s/LOG_FILE_PATH_CGI = cgiphp.log/LOG_FILE_PATH_CGI = \/var\/log\/php\/cgiphp.log/" \!config.ini > config.new
mv -f config.new \!config.ini
sed "s/LAMPCMS_PATH =\"\/\"/LAMPCMS_PATH =\"\/var\/www\"/" \!config.ini > config.new
mv -f config.new \!config.ini
sed "s/LAMPCMS_DATA_DIR =/LAMPCMS_DATA_DIR =\"\/var\/www\/html\/w\"/" \!config.ini > config.new
mv -f config.new \!config.ini
sed "s/CATEGORIES = 2/CATEGORIES = 1/" \!config.ini > config.new
mv -f config.new \!config.ini
sed "s/;twitter/twitter/" \!config.ini > config.new
mv -f config.new \!config.ini
sed "s/;facebook/facebook/" \!config.ini > config.new
mv -f config.new \!config.ini
sed "s/;linkedin/linkedin/" \!config.ini > config.new
mv -f config.new \!config.ini
sed "s/# RewriteEngine on/RewriteEngine on/" RewriteRules.txt > /etc/httpd/conf.d/lampcms.conf


# restart Apache
echo Restarting Apache ...
service httpd restart
##Starting httpd:                                            [  OK  ]

