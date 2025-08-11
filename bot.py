import os
import telebot
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from telebot import types

TOKEN = os.getenv("TELEGRAM_TOKEN", "8062995274:AAErOwOGL090cuu9ZOjWeBOt7ym9ydrRV9w")
bot = telebot.TeleBot(TOKEN)

# تخزين driver و بيانات المستخدم
driver = None
user_data = {}

def setup_driver():
    global driver
    if driver is not None:
        return driver

    gecko_path = "/usr/bin/geckodriver"
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    service = Service(executable_path=gecko_path)
    driver = webdriver.Firefox(service=service, options=options)
    driver.get("https://db-iraq.gomail.gay")

    # انتظر تحميل الحقول
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "fname")))
    return driver

@bot.message_handler(commands=["start"])
def send_welcome(message):
    setup_driver()
    bot.send_message(message.chat.id, "أرسل الاسم الثلاثي (الاسم الأول، الثاني، الثالث) مفصول بمسافات:")

@bot.message_handler(func=lambda m: True)
def handle_name_and_state(message):
    chat_id = message.chat.id

    if chat_id not in user_data:
        # نتوقع الاسم الثلاثي
        parts = message.text.strip().split()
        if len(parts) != 3:
            bot.send_message(chat_id, "الرجاء إرسال الاسم الثلاثي بالضبط (3 كلمات مفصولة بمسافات). حاول مرة أخرى:")
            return

        # خزّن الاسم
        user_data[chat_id] = {
            "fname": parts[0],
            "lname": parts[1],
            "tname": parts[2]
        }

        # أدخل الأسماء في الموقع
        driver = setup_driver()
        driver.find_element(By.ID, "fname").clear()
        driver.find_element(By.ID, "fname").send_keys(parts[0])

        driver.find_element(By.ID, "lname").clear()
        driver.find_element(By.ID, "lname").send_keys(parts[1])

        driver.find_element(By.ID, "tname").clear()
        driver.find_element(By.ID, "tname").send_keys(parts[2])

        # إرسال خيارات المحافظات
        markup = types.ReplyKeyboardMarkup(row_width=3, one_time_keyboard=True, resize_keyboard=True)
        provinces = [
            ("بغداد", "baghdad"), ("الانبار", "anbar"), ("بابل", "babel"),
            ("بلد - سامراء", "balad"), ("البصرة", "basra"), ("ذي قار", "theqar"),
            ("ديالى", "dyala"), ("دهوك", "dhuk"), ("اربيل", "arbil"),
            ("كربلاء", "karblaa"), ("كركوك", "kirkuk"), ("ميسان", "mesan"),
            ("مُثنى", "muthana"), ("نجف", "najaf"), ("نينوى", "nynoa"),
            ("الديوانية (القادسية)", "qadisiah"), ("صلاح الدين", "salah-aldien"),
            ("واسط", "wasit"), ("سُليمانية", "sulimaniah")
        ]

        for name, val in provinces:
            markup.add(types.KeyboardButton(name))

        bot.send_message(chat_id, "اختر المحافظة:", reply_markup=markup)

    else:
        # نتوقع المحافظة
        province_map = {
            "بغداد": "baghdad", "الانبار": "anbar", "بابل": "babel",
            "بلد - سامراء": "balad", "البصرة": "basra", "ذي قار": "theqar",
            "ديالى": "dyala", "دهوك": "dhuk", "اربيل": "arbil",
            "كربلاء": "karblaa", "كركوك": "kirkuk", "ميسان": "mesan",
            "مُثنى": "muthana", "نجف": "najaf", "نينوى": "nynoa",
            "الديوانية (القادسية)": "qadisiah", "صلاح الدين": "salah-aldien",
            "واسط": "wasit", "سُليمانية": "sulimaniah"
        }

        province_val = province_map.get(message.text)
        if not province_val:
            bot.send_message(chat_id, "اختر المحافظة من القائمة فقط.")
            return

        # أدخل المحافظة في الـ select بالموقع
        driver = setup_driver()
        select_element = driver.find_element(By.ID, "state")
        select = Select(select_element)
        select.select_by_value(province_val)

        bot.send_message(chat_id, f"تم اختيار المحافظة: {message.text} ✅\nيمكنك الآن المتابعة بالعمليات المطلوبة.")
        # يمكن هنا إضافة وظائف إضافية أو إعادة ضبط user_data للبدء من جديد
        user_data.pop(chat_id, None)

if __name__ == "__main__":
    print("Bot is running...")
    bot.polling()
