import os
import telebot
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
import time

# ===== إعداد البوت =====
TOKEN = os.getenv("TELEGRAM_TOKEN", "8062995274:AAErOwOGL090cuu9ZOjWeBOt7ym9ydrRV9w")
bot = telebot.TeleBot(TOKEN)

# ===== إعداد Selenium =====
def setup_driver():
    try:
        gecko_path = "/usr/bin/geckodriver"
        if not os.path.exists(gecko_path):
            raise Exception(f"geckodriver غير موجود في {gecko_path}")

        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        service = Service(executable_path=gecko_path)
        driver = webdriver.Firefox(service=service, options=options)
        return driver
    except Exception as e:
        raise Exception(f"خطأ في إعداد Selenium: {str(e)}")

# ===== دالة جلب السعر =====
def get_dollar_price():
    driver = setup_driver()
    try:
        driver.get("https://www.xe.com/currencyconverter/convert/?Amount=1&From=USD&To=IQD")
        time.sleep(5)  # انتظار تحميل الصفحة

        # جلب النص من العنصر الذي يحتوي على السعر
        price_element = driver.find_element(By.XPATH, '//p[@class="result__BigRate-sc-1bsijpp-1 iGrAod"]')
        price = price_element.text
        return f"💵 سعر الدولار اليوم: {price}"
    except Exception as e:
        return f"حدث خطأ: {str(e)}"
    finally:
        driver.quit()

# ===== أوامر البوت =====
@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.reply_to(message, "أهلاً! أرسل /price لجلب سعر الدولار.")

@bot.message_handler(commands=["price"])
def send_price(message):
    bot.reply_to(message, "⏳ جاري جلب السعر...")
    result = get_dollar_price()
    bot.send_message(message.chat.id, result)

# ===== تشغيل البوت =====
if __name__ == "__main__":
    print("Bot is running...")
    bot.polling()
