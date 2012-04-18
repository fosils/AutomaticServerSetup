from fabric import context_managers as cm
from fabric import operations as op

def replace_in_file(file, before, after):
    op.run("sudo sed --in-place 's|%s|%s|' '%s'" % (before, after, file))

def replace_in_config_ini(before, after):
    replace_in_file('/var/www/!config.ini', before, after)

def run(aws):
    # install pdo_mysql PHP extension if it isn't already installed (lib* because it's either in /usr/lib/ or /usr/lib64/)
    op.run('sudo yum -y install mysql-devel php-pdo')
    op.run('[ -f /usr/lib*/php/modules/pdo_mysql.so ] || sudo pecl install pdo_mysql')
    op.run('echo "extension=pdo_mysql.so" | sudo tee /etc/php.d/pdo_mysql.ini > /dev/null')

    # create LampCMS database in Mysql
    op.run('echo Creating LampCMS database ...')
    input = ('create database LAMPCMS; ' +
             'create user ' + aws.options.mysql_lamp_user + ' identified by "' + aws.options.mysql_lamp_pw + '"; ' +
             'grant all privileges on LAMPCMS.* to ' + aws.options.mysql_lamp_user + ' with grant option; ')
    op.run('echo \'' + input + '\' | mysql -u root mysql --password=' + aws.options.mysql_root_pw + ' || true')

    # download LampCMS package
    op.run('echo Downloading LampCMS package ...')
    op.run('sudo rm -rf /tmp/tmp')
    op.run('mkdir /tmp/tmp')
    op.run('wget -O /tmp/tmp/lampcms.zip -o /dev/null https://github.com/fosils/LampCMS-for-Open-org.com/zipball/master')

    # install LampCMS (install_lampcms.sh)
    op.run('echo Installing LampCMS ...')
    with cm.cd('/tmp/tmp'):
        op.run('unzip lampcms.zip > /dev/null')
        op.run('rm -f lampcms.zip')
        op.run('sudo rm -f /var/www/www')
        op.run('sudo cp -Rf /tmp/tmp/*/* /var/www')
    op.run('rm -rf /tmp/tmp/*')
    with cm.cd('/var/www'):
        op.run('sudo rm -rf html')
        op.run('sudo mv www html')
        op.run('sudo ln -s html www')
    op.run('sudo mkdir -p /var/www/html/w/img/tmp /var/log/php')
    op.run('sudo chown -R apache /var/www/www/w')
    op.run('sudo chown apache /var/log/php')

    # download openorg-aws-setup
    op.run('echo Downloading openorg-aws-setup ...')
    with cm.cd('/var/www'):
        op.run('sudo rm -fr openorg-aws-setup')
        op.run('sudo git clone git://github.com/fosils/openorg-aws-setup.git')
        op.run('sudo mv openorg-aws-setup/startsandbox.php /var/www/html/')
        op.run('sudo chown apache openorg-aws-setup/')

    # configure LampCMS (config_lampcms.sh)
    op.run('echo Configuring LampCMS ...')
    with cm.cd('/var/www'):
        op.run('sudo mv -f \!config.ini.dist \!config.ini')
        op.run('sudo mv -f acl.ini.dist acl.ini')
        op.run('sudo mv -f Points.php.dist Points.php')
        op.run('sudo mv -f Mycollections.php.dist Mycollections.php')

    # create the MySQL table, since the LampCMS code doesn't seem to be able to
    with cm.cd('/var/www/lib/Lampcms/Modules/Search/'):
        op.run("php -r 'require \"TitleTagsTable.php\"; " +
               "        $x = new Lampcms\Modules\Search\TitleTagsTable(); " +
               "        print $x::SQL;' | " +
               "mysql -u " + aws.options.mysql_lamp_user + " LAMPCMS --password=" + aws.options.mysql_lamp_pw + " || true")

    # work around a bug that expects TitleTagsTable.php to be in the wrong place
    # (not needed if we're creating the table here)
    # op.run("sudo ln -s Modules/Search/TitleTagsTable.php /var/www/lib/Lampcms/")

    replace_in_config_ini('TCP_Port_number=',               'TCP_Port_number = 3306')
    replace_in_config_ini('Database_username=',             'Database_username = ' + aws.options.mysql_lamp_user)
    replace_in_config_ini('Database_password=',             'Database_password = ' + aws.options.mysql_lamp_pw)
    replace_in_config_ini('DEBUG = true',                   'DEBUG = false')
    replace_in_config_ini('LOG_FILE_PATH = php.log',        'LOG_FILE_PATH = /var/log/php/php.log')
    replace_in_config_ini('LOG_FILE_PATH_CGI = cgiphp.log', 'LOG_FILE_PATH_CGI = /var/log/php/cgiphp.log')
    replace_in_config_ini('SITE_URL="http://localhost"',    'SITE_URL = "http://' + aws.hostname + '"')
    replace_in_config_ini('LAMPCMS_PATH ="/"',              'LAMPCMS_PATH = "/var/www"')
    replace_in_config_ini('LAMPCMS_DATA_DIR =',             'LAMPCMS_DATA_DIR = "/var/www/html/w"')
    replace_in_config_ini('EMAIL_DEVELOPER = "me@me.me"',   'EMAIL_DEVELOPER = "' + aws.options.admin_email + '"')
    replace_in_config_ini('EMAIL_ADMIN = "me@me.me"',       'EMAIL_ADMIN = "' + aws.options.admin_email + '"')
    replace_in_config_ini('^CATEGORIES = ',                 'CATEGORIES = ')
    replace_in_config_ini(';twitter',                       'twitter')
    replace_in_config_ini(';facebook',                      'facebook')
    replace_in_config_ini(';linkedin',                      'linkedin')

    op.run('sed "s/# RewriteEngine on/RewriteEngine on/" /var/www/RewriteRules.txt | sudo tee /etc/httpd/conf.d/lampcms.conf > /dev/null')
