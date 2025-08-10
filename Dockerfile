FROM python:3.11-slim

# تثبيت المتطلبات الأساسية
RUN apt-get update && apt-get install -y \
    wget tar firefox-esr ca-certificates \
    libgtk-3-0 libdbus-glib-1-2 libasound2 \
    --no-install-recommends && rm -rf /var/lib/apt/lists/*

# تثبيت geckodriver
ENV GECKO_VER=0.34.0
RUN wget -q "https://github.com/mozilla/geckodriver/releases/download/v${GECKO_VER}/geckodriver-v${GECKO_VER}-linux64.tar.gz" -O /tmp/geckodriver.tar.gz && \
    tar -xzf /tmp/geckodriver.tar.gz -C /tmp && \
    mv /tmp/geckodriver /usr/bin/geckodriver && \
    chmod +x /usr/bin/geckodriver && \
    rm /tmp/geckodriver.tar.gz

# إعداد مجلد العمل
WORKDIR /app
COPY . /app

# تثبيت مكتبات بايثون
RUN pip install --no-cache-dir -r requirements.txt

# متغيرات بيئة
ENV PATH="/usr/bin:${PATH}"

# تشغيل البوت
CMD ["python", "bot.py"]
