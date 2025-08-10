#!/bin/bash

# تثبيت المتطلبات الأساسية
apt-get update
apt-get install -y wget tar firefox-esr

# تحميل وتثبيت geckodriver (بإصدار حديث)
wget https://github.com/mozilla/geckodriver/releases/download/v0.34.0/geckodriver-v0.34.0-linux64.tar.gz
tar -xvzf geckodriver-*.tar.gz
chmod +x geckodriver

# تثبيت في مسار بديل (أكثر موثوقية)
mv geckodriver /app/.apt/usr/bin/
ln -s /app/.apt/usr/bin/geckodriver /usr/bin/geckodriver

# التحقق من التثبيت
echo "مسار geckodriver: $(which geckodriver)"
echo "إصدار geckodriver: $(geckodriver --version)"
echo "إصدار Firefox: $(firefox --version)"

# تشغيل البوت
python bot.py