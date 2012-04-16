import os, time
import base64
import boto.ec2
import fabric.api
import sys

aws_key_id=''
aws_secret=''
region='eu-west-1'

class aws_tool(object):
    '''
    
    '''
    groupname = 'def-generated-group'
    groupdesc = 'Default security group with ssh and http access.'
    key_directory = './'
    scripts_dir = './scripts/'
    instance_size = 't1.micro'
    ami_name = 'ami-fd231b89' # Amazon Linux AMI 2012.03, i386

    def __init__(self, aws_key, aws_secret, region):
        self.aws_key = aws_key
        self.aws_secret = aws_secret
        self.region = region
        
        self.ec2 = boto.ec2.connect_to_region(region,
                                              aws_access_key_id=self.aws_key,
                                              aws_secret_access_key=self.aws_secret)

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

    def start_instance(self):
        self.generate_key()
        self.generate_sec_group()
        ami =  self.ec2.get_all_images([self.ami_name])[0]
        self.reservation = ami.run(key_name=self.keyname,
                                   instance_type=self.instance_size,
                                   security_groups=[self.group])
        self.reservation = self.reservation.instances[0]
        while self.reservation.update() != u'running':
            time.sleep(1)
        print 'AWS instance set up at', self.reservation.public_dns_name        
        fabric.api.env.host_string = 'ec2-user@%s' % self.reservation.public_dns_name
        fabric.api.env.key_filename = self.key_directory + self.keyname +'.pem'

    def run_tasks(self, tasks):
        for t in tasks:
            a = __import__('tasks.%s' % (t),None,None,'run')
            a.run(self)

    def gen_key_prefix(self):
        return self.random_letters(6)

    def random_letters(self, count):
        return base64.urlsafe_b64encode(os.urandom(count))

if __name__ == '__main__':
    if len(sys.argv) != 3:  # the program name and the two arguments
        # stop the program and print an error message
        sys.exit("You must provide two parameters: AWS Key ID and AWS Secret Key")
    aws_key_id = sys.argv[1]
    aws_secret = sys.argv[2]
    aws = aws_tool(aws_key_id, aws_secret, region)
    aws.start_instance()
    print "Waiting for instance to boot..."
    time.sleep(120)
    aws.run_tasks(['update_packages','setup_python','lampcms'])
