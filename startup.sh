#!/bin/bash

# تثبيت المتطلبات
apt-get update
apt-get install -y wget tar firefox-esr

# تحميل geckodriver
wget https://github.com/mozilla/geckodriver/releases/download/v0.34.0/geckodriver-v0.34.0-linux64.tar.gz
tar -xvzf geckodriver-*.tar.gz
chmod +x geckodriver
mv geckodriver /usr/bin/

# تشغيل البوت
python bot.py