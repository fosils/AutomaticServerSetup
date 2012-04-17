#!/bin/bash

# download QandA package
cd /var/www/html
echo Downloading QandA package ...
wget -qO - https://github.com/dkode/QA-website/tarball/master | tar -xz

# install QA
echo Installing QA-website
mv -f dkode-QA-*/* ./
rmdir dkode-QA-*
