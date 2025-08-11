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
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "fname")))
    return driver

@bot.message_handler(commands=["start"])
def send_welcome(message):
    setup_driver()
    bot.send_message(message.chat.id, "أرسل الاسم (ثنائي أو ثلاثي) مفصول بمسافات:")

@bot.message_handler(func=lambda m: True)
def handle_all(message):
    chat_id = message.chat.id

    if chat_id not in user_data:
        # استقبال الاسم (ثنائي أو ثلاثي)
        parts = message.text.strip().split()
        if len(parts) < 2 or len(parts) > 3:
            bot.send_message(chat_id, "الرجاء إرسال اسم ثنائي أو ثلاثي فقط (كلمتين أو ثلاث كلمات). حاول مرة أخرى:")
            return

        # حفظ الاسم مع تعيين القيم
        fname = parts[0]
        lname = parts[1]
        tname = parts[2] if len(parts) == 3 else ""

        user_data[chat_id] = {
            "fname": fname,
            "lname": lname,
            "tname": tname,
            "age": None,
            "province": None
        }

        bot.send_message(chat_id, "الآن اختر سنة الميلاد أو اكتب 'لا' للتخطي:", reply_markup=age_keyboard())

    elif user_data[chat_id]["age"] is None:
        # استقبال سنة الميلاد أو 'لا' للتخطي
        text = message.text.strip()
        if text == "لا":
            user_data[chat_id]["age"] = ""
        else:
            valid_ages = [str(year) for year in range(1900, 2023)]
            if text not in valid_ages:
                bot.send_message(chat_id, "اختر سنة الميلاد من القائمة أو اكتب 'لا' للتخطي.")
                bot.send_message(chat_id, "اختار سنة الميلاد:", reply_markup=age_keyboard())
                return
            user_data[chat_id]["age"] = text

        # بعد العمر، عرض المحافظات
        bot.send_message(chat_id, "اختر المحافظة:", reply_markup=province_keyboard())

    elif user_data[chat_id]["province"] is None:
        # استقبال المحافظة
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
            bot.send_message(chat_id, "اختر المحافظة من القائمة فقط.", reply_markup=province_keyboard())
            return

        user_data[chat_id]["province"] = province_val

        # الآن نملأ البيانات في الموقع عبر Selenium
        driver = setup_driver()
        driver.find_element(By.ID, "fname").clear()
        driver.find_element(By.ID, "fname").send_keys(user_data[chat_id]["fname"])

        driver.find_element(By.ID, "lname").clear()
        driver.find_element(By.ID, "lname").send_keys(user_data[chat_id]["lname"])

        driver.find_element(By.ID, "tname").clear()
        driver.find_element(By.ID, "tname").send_keys(user_data[chat_id]["tname"])

        # اختيار العمر إذا موجود
        age_value = user_data[chat_id]["age"]
        select_age = Select(driver.find_element(By.ID, "age"))
        if age_value:
            try:
                select_age.select_by_value(age_value)
            except:
                pass  # إذا لم يجد القيمة لا يختار شيء

        # اختيار المحافظة
        select_province = Select(driver.find_element(By.ID, "state"))
        select_province.select_by_value(province_val)

        bot.send_message(chat_id, "تم تعبئة البيانات بنجاح! يمكنك المتابعة الآن.")
        user_data.pop(chat_id, None)  # إعادة تعيين الجلسة

def age_keyboard():
    markup = types.ReplyKeyboardMarkup(row_width=5, one_time_keyboard=True, resize_keyboard=True)
    years = [str(y) for y in range(1900, 2023)]
    # عرض سنوات على دفعات 25 سنة لكل صف لتجنب طول القائمة
    for i in range(0, len(years), 25):
        markup.row(*years[i:i+25])
    markup.add(types.KeyboardButton("لا"))  # خيار تخطي
    return markup

def province_keyboard():
    markup = types.ReplyKeyboardMarkup(row_width=3, one_time_keyboard=True, resize_keyboard=True)
    provinces = [
        "بغداد", "الانبار", "بابل", "بلد - سامراء", "البصرة", "ذي قار",
        "ديالى", "دهوك", "اربيل", "كربلاء", "كركوك", "ميسان",
        "مُثنى", "نجف", "نينوى", "الديوانية (القادسية)", "صلاح الدين",
        "واسط", "سُليمانية"
    ]
    for p in provinces:
        markup.add(types.KeyboardButton(p))
    return markup

if __name__ == "__main__":
    print("Bot is running...")
    bot.polling()
