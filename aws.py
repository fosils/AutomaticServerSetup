import os, time
import base64
import boto.ec2
import fabric.api
import string
import sys

from optparse import OptionParser

# default passwords and other parameters - can override with command line parameters,
# for example:
#    aws.py --mysql-root-pw=fred --admin_email=someone@somewhere.com ABCDEFG werwer+werwer
#
# specify --host and --keyfile to connect to an existing instance rather than making a new one
#
#    aws.py -h		will show all available command line parameters

# AWS instance root password
aws_root_pw = 'pleasechangethispassword912'

# Mysql root password
mysql_root_pw = 'root'

# username and password to connect LampCMS database
mysql_lamp_user = 'lampcms'
mysql_lamp_pw   = 'lampcms_pass'

# LampCMS administrator email
admin_email = 'root@lampcms.net'

host = ''
keyfile = ''
aws_key_id = ''
aws_secret = ''
region = 'us-east-1'

class aws_tool(object):
    '''
    
    '''
    groupname = 'def-generated-group'
    groupdesc = 'Default security group with ssh and http access.'
    key_directory = './'
    scripts_dir = './scripts/'
    instance_size = 't1.micro'
    ami_name = 'ami-e565ba8c' # Amazon Linux AMI 2012.03, x86_64

    def __init__(self, region):
        self.parse_options()
        self.aws_key = self.args[0]
        self.aws_secret = self.args[1]
        self.region = region
        self.tasks = {}
        
        self.ec2 = boto.ec2.connect_to_region(region,
                                              aws_access_key_id=self.aws_key,
                                              aws_secret_access_key=self.aws_secret)

    def parse_options(self):
        parser = OptionParser()
        parser.add_option("--host", default = host)
        parser.add_option("--keyfile", default = keyfile)
        parser.add_option("--aws-root-pw", default = aws_root_pw)
        parser.add_option("--mysql-root-pw", default = mysql_root_pw)
        parser.add_option("--mysql-lamp-user", default = mysql_lamp_user)
        parser.add_option("--mysql-lamp-pw", default = mysql_lamp_pw)
        parser.add_option("--admin-email", default = admin_email)
        parser.add_option("--task", action = "append")
        (self.options, self.args) = parser.parse_args()

        if len(self.args) != 2:  # we need the two keys
            # stop the program and print an error message
            sys.exit("You must provide two parameters: AWS Key ID and AWS Secret Key")

    def random_letters(self, count):
        return base64.urlsafe_b64encode(os.urandom(count))

    def gen_key_prefix(self):
        return self.random_letters(6)

    def generate_key(self):
        self.keyname = 'generated-key-%s' % self.gen_key_prefix()
        kp = self.ec2.create_key_pair(self.keyname)
        kp.save(self.key_directory)

    def generate_sec_group(self):
        try:
            self.group = self.ec2.create_security_group(self.groupname, self.groupdesc)
        except:
            self.group = self.ec2.get_all_security_groups(self.groupname)[0]
            return
        self.group.authorize(ip_protocol='tcp', from_port='22', to_port='22', cidr_ip='0.0.0.0/0')
        self.group.authorize(ip_protocol='tcp', from_port='80', to_port='80', cidr_ip='0.0.0.0/0')

    def show_credentials(self):
        print("\n  NOTE: you can reconnect to this instance later by specifying flags:\n    --keyfile %s --host %s" %
              (fabric.api.env.key_filename, self.hostname))
        print("\n  NOTE: you can log in to this instance by running:\n    ssh -i %s %s" %
              (fabric.api.env.key_filename, fabric.api.env.host_string))
        print("\n  NOTE: if the instance is serving a web page, you can view it here:\n    http://%s/\n" %
              (self.hostname,))

    def start_instance(self):
        self.generate_key()
        self.generate_sec_group()
        ami =  self.ec2.get_all_images([self.ami_name])[0]
        sys.stdout.write("Setting up new AWS instance: ")
        self.reservation = ami.run(key_name=self.keyname,
                                   instance_type=self.instance_size,
                                   security_groups=[self.group])
        self.reservation = self.reservation.instances[0]
        while True:
            time.sleep(3)
            if (self.reservation.update() == u'running'):
                break
            sys.stdout.write('.')
            sys.stdout.flush()
        print

        self.hostname = self.reservation.public_dns_name
        fabric.api.env.host_string = 'ec2-user@%s' % self.hostname
        fabric.api.env.key_filename = self.key_directory + self.keyname +'.pem'
        self.show_credentials()
        aws.run_task('wait_for_boot')

    def use_existing_instance(self, host_string, key_filename):
        # if they included the 'ec2-user@' prefix, remove it
        host_string = string.split(host_string, '@')[-1]
        fabric.api.env.host_string = 'ec2-user@%s' % host_string
        fabric.api.env.key_filename = key_filename
        self.hostname = host_string
        
    def run_task(self, task, force = False):
        # only run each task once, unless force==True
        if (force or not self.tasks.has_key(task)):
            self.tasks[task] = True
            try:
                a = __import__('tasks.%s' % (task),None,None,'run')
            except ImportError:
                print "Can't import task '%s': %s" % (task, sys.exc_info()[1])
                sys.exit(1)
            a.run(self)
        else:
            print "skipping task '%s' because it was already run" % task

    def run_tasks(self, tasks, force = False):
        for task in tasks:
            self.run_task(task, force)

if __name__ == '__main__':
    aws = aws_tool(region)

    if (aws.options.host and aws.options.keyfile):
        aws.use_existing_instance(aws.options.host, aws.options.keyfile)
    else:
        aws.start_instance()

    if (aws.options.task):
        aws.run_tasks(aws.options.task)
    else:
        aws.run_tasks(['lampcms'])

    aws.show_credentials()
