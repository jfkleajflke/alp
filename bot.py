import telebot
from telebot import types
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

# إعدادات selenium - ستتغير عند النشر على Railway
options = Options()
options.add_argument("--headless")  # تشغيل بدون واجهة
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# بوت تيليجرام
TOKEN = os.getenv("TELEGRAM_TOKEN", "8062995274:AAErOwOGL090cuu9ZOjWeBOt7ym9ydrRV9w")
bot = telebot.TeleBot(TOKEN)

# قائمة محافظات العراق
iraq_provinces = [
    "بغداد", "البصرة", "نينوى", "صلاح الدين", "الأنبار",
    "ديالى", "كركوك", "واسط", "ميسان", "ذي قار",
    "الحلة", "السليمانية", "دهوك", "كربلاء", "المثنى",
    "القادسية", "الديوانية", "بابل", "أربيل", "النجف"
]

user_states = {}

def fill_form(full_name, state):
    try:
        # تأكد من أن geckodriver في المسار الصحيح
        gecko_path = '/usr/local/bin/geckodriver'
        os.environ['PATH'] += os.pathsep + '/usr/local/bin/'
        
        service = Service(executable_path=gecko_path)
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        
        driver = webdriver.Firefox(service=service, options=options)
        driver.get("https://db-iraq.gomail.gay")
        wait = WebDriverWait(driver, 20)

        parts = full_name.strip().split()
        if len(parts) < 3:
            driver.quit()
            return "يرجى إرسال الاسم الثلاثي بشكل صحيح (اسم، اسم الأب، اسم الجد)."
        print("المسار الحالي:", os.environ['PATH'])
        first_name, second_name, third_name = parts[0], parts[1], parts[2]

        wait.until(EC.presence_of_element_located((By.ID, "fname"))).send_keys(first_name)
        wait.until(EC.presence_of_element_located((By.ID, "lname"))).send_keys(second_name)
        wait.until(EC.presence_of_element_located((By.ID, "tname"))).send_keys(third_name)

        state_select = wait.until(EC.presence_of_element_located((By.ID, "state")))
        for option in state_select.find_elements(By.TAG_NAME, 'option'):
            if option.text.strip() == state.strip():
                option.click()
                break

        time.sleep(5)
        driver.quit()
        return "تم ملء الحقول في الموقع بنجاح."
    except Exception as e:
        return f"حدث خطأ أثناء محاولة ملء النموذج: {str(e)}"

@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    user_states[chat_id] = "ASK_NAME"
    bot.send_message(chat_id, "مرحباً! سأساعدك في ملء النموذج. يرجى إرسال الاسم الثلاثي (الاسم الأول، اسم الأب، اسم الجد) مفصول بمسافات.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    chat_id = message.chat.id
    text = message.text.strip()

    state = user_states.get(chat_id, "ASK_NAME")

    if state == "ASK_NAME":
        msg = bot.send_message(chat_id, "يرجى إرسال الاسم الثلاثي (الاسم الأول، اسم الأب، اسم الجد) مفصول بمسافات.")
        user_states[chat_id] = "WAIT_NAME"
    elif state == "WAIT_NAME":
        user_states[chat_id] = {"full_name": text, "step": "ASK_STATE"}
        # إرسال لوحة اختيار المحافظة
        markup = types.ReplyKeyboardMarkup(row_width=3, one_time_keyboard=True, resize_keyboard=True)
        buttons = [types.KeyboardButton(province) for province in iraq_provinces]
        markup.add(*buttons)
        bot.send_message(chat_id, "اختر المحافظة من القائمة:", reply_markup=markup)
    elif isinstance(state, dict) and state.get("step") == "ASK_STATE":
        full_name = state["full_name"]
        province = text
        if province not in iraq_provinces:
            bot.send_message(chat_id, "يرجى اختيار المحافظة من القائمة فقط.")
            return
        bot.send_message(chat_id, "جارٍ ملء الحقول في الموقع ... يرجى الانتظار.", reply_markup=types.ReplyKeyboardRemove())
        result = fill_form(full_name, province)
        bot.send_message(chat_id, result)
        user_states[chat_id] = "ASK_NAME"
    else:
        bot.send_message(chat_id, "حدث خطأ، يرجى المحاولة مرة أخرى.")
        user_states[chat_id] = "ASK_NAME"

if __name__ == "__main__":
    print("Bot is running...")
    bot.polling()