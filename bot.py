import os
import telebot
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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

# ===== دالة التحقق من وجود الحقول =====
def check_form_fields():
    driver = None
    try:
        driver = setup_driver()
        driver.get("https://db-iraq.gomail.gay")

        # انتظر حتى يظهر الحقل الأول
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "fname"))
        )

        # جلب العناصر
        driver.find_element(By.ID, "fname")
        driver.find_element(By.ID, "lname")
        driver.find_element(By.ID, "tname")

        return "الحقول fname, lname, tname موجودة ✅"

    except Exception as e:
        return f"الحقول غير موجودة أو حدث خطأ: {str(e)}"
    finally:
        if driver:
            driver.quit()

# ===== أوامر البوت =====
@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.reply_to(message, "أهلاً! أرسل /checkform للتحقق من وجود حقول الاسم في الموقع.")

@bot.message_handler(commands=["checkform"])
def check_form_command(message):
    bot.reply_to(message, "⏳ جاري التحقق من الحقول...")
    result = check_form_fields()
    bot.send_message(message.chat.id, result)

# ===== تشغيل البوت =====
if __name__ == "__main__":
    print("Bot is running...")
    bot.polling()
