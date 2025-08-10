#!/bin/bash

# تثبيت المتطلبات الأساسية للـ Chrome
apt-get update
apt-get install -y wget gnupg

# تثبيت Chrome
wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list
apt-get update
apt-get install -y google-chrome-stable

# تثبيت chromedriver
CHROME_VERSION=$(google-chrome --version | awk '{print $3}' | cut -d '.' -f 1)
wget https://chromedriver.storage.googleapis.com/LATEST_RELEASE_${CHROME_VERSION} -O chromedriver_version.txt
CHROMEDRIVER_VERSION=$(cat chromedriver_version.txt)
wget https://chromedriver.storage.googleapis.com/${CHROMEDRIVER_VERSION}/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
chmod +x chromedriver
mv chromedriver /usr/local/bin/

# تشغيل البوت
python bot.py