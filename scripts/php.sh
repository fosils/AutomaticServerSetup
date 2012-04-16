
# install PHP
echo Installing PHP and modules ...
yum -y install php php-devel php-mbstring php-pecl-apc php-pecl-oauth php-gd php-xml re2c
##Complete!


# install GCC compiler and Make
echo Installing GCC compiler ...
yum -y install gcc make
##Complete!

#update pecl channel
pecl channel-update pecl.php.net
