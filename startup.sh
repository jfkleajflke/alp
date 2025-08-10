#!/bin/bash

# تثبيت المتطلبات الأساسية
apt-get update
apt-get install -y wget tar firefox-esr

# تحميل وتثبيت geckodriver
wget https://github.com/mozilla/geckodriver/releases/download/v0.33.0/geckodriver-v0.33.0-linux64.tar.gz
tar -xvzf geckodriver*.tar.gz
chmod +x geckodriver
mv geckodriver /usr/local/bin/

# تصدير المسار للتأكد
export PATH=$PATH:/usr/local/bin/

# تشغيل البوت
python bot.py