<?php
function show_form() {
?>
<ul>
<li><a href="http://forum.open-org.com/q293/How-to-start-using-EC2">Learn how to sign up with Amazon Web Services</a>
<li><a href="https://aws-portal.amazon.com/gp/aws/securityCredentials">Find your AWS keys here</a>
</ul>

<form method="post">
Access Key ID: <input type="text" name="keyid" /><br />
Secret Access Key: <input type="text" name="secret" /><br />
<input type="submit" value="Give me a sandbox server now" />
</form>
<?php
}

function clean_string($str) {
    return preg_replace("|[^A-Za-z0-9+/]|", "", $str);
}

function post($str) {
    return clean_string($_POST[$str]);
}

?>

<html>
<body>
<?php
if (isset($_POST['keyid']) && isset($_POST['secret'])) {
    $keyid = post('keyid');
    $secret = post('secret');
    chdir("/var/www/openorg-aws-setup/");
    $command = "python aws.py $keyid $secret 2>&1";
    # $command = "./script.sh";
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
        print "new server is up at <a href=\"$url\">$url</a>.<br />\n";
} else {
    show_form();
}
?>
</body>
</html>
