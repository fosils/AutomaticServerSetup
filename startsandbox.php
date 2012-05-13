<?php
function show_form($email, $keyid, $secret) {
?>
<!--
<ul>
<li><a target="_blank" href="http://forum.open-org.com/q293/How-to-start-using-EC2">Learn how to sign up with Amazon Web Services</a>
<li><a target="_blank" href="https://aws-portal.amazon.com/gp/aws/securityCredentials">Find your AWS keys here</a>
</ul>
-->

<form method="post">
Email Address: <input type="text" name="email" value="<?php print $email;?>" /><br />
SSH root password: <input type="password" name="pass" /><br />
SSH root password again: <input type="password" name="pass2" /><br />
Amazon Access Key ID: <input type="text" name="keyid" value="<?php print $keyid;?>" /><br />
Amazon Secret Access Key: <input type="text" name="secret" value="<?php print $secret;?>" /><br />
<input type="hidden" name="form" value="1"/><br />
<input type="submit" value="Give me a sandbox server now" />
</form>
<?php
}

function clean_string($str) {
    return preg_replace("|[^A-Za-z0-9@+/.,_-]|", "", $str);
}

function post($str) {
    return clean_string($_POST[$str]);
}

?>

<html>
<body>
<?php
$bad = false;
if (!isset($_POST['form'])) {
    $bad = true;
    $email = $keyid = $secret = '';
} else {
    $email = post('email');
    $pass = post('pass');
    $pass2 = post('pass2');
    $keyid = post('keyid');
    $secret = post('secret');

    if ($email == '') {
        print "you didn't specify your email address<br/>\n";
        $bad = true;
    }

    if ($pass == '') {
        print "you didn't specify a password to use for the instance<br/>\n";
        $bad = true;
    } else if ($pass2 == '') {
        print "you didn't specify your password a 2nd time<br/>\n";
        $bad = true;
    } else if ($_POST['pass'] != $_POST['pass2']) {
        print "the two passwords don't match<br/>\n";
        $bad = true;
    } else if ($pass != $_POST['pass']) {
        print "the password should only contain A-Z, a-z, 0-9, and any of @+/.,_-<br/>\n";
        $bad = true;
    }

    if ($keyid == '') {
        print "you didn't specify your AWS key id<br/>\n";
        $bad = true;
    }

    if ($secret == '') {
        print "you didn't specify your AWS secret<br/>\n";
        $bad = true;
    }
}

if ($bad) {
    print "<br/>\n";
    show_form($email, $keyid, $secret);
} else {
    chdir("/var/www/openorg-aws-setup/");
    $command = "python aws.py --admin-email $email --aws-root-pw $pass --task lampcms --task sshd $keyid $secret 2>&1";
    print "setting up sandbox server.<br />it takes a couple of minutes to create a new instance, then shows output in real time:<br />\n";
    ob_flush(); flush(); 
    $fp = popen($command, 'r');
    print "<pre>\n";
    $url = false;
    while (!feof($fp)) { 
        $line = fgets($fp);
        if (!$url)
            // AWS instance set up at ec2-79-125-88-90.eu-west-1.compute.amazonaws.com
            if (preg_match("/^AWS instance set up at (.*)$/", $line, $matches)) {
                $url = $matches[1];
                $url = "http://$url/";
                // print "url: $url\n";
            }
        print $line;
        ob_flush(); flush(); 
    } 
    fclose($fp);
    print "</pre>\n";
    print "done.<br />\n";
    if ($url)
        print "new server is up at <a href=\"$url\">$url</a>. You can either access the server via the browser or SSH using the password you provided.<br />\n";
}
?>
</body>
</html>
