import telebot
from flask import Flask
from threading import Thread
import os # Bu mütləq olmalıdır!

# 1. Tokeni Render-in 'Environment Variables' hissəsindən oxuyur
TOKEN = os.environ.get('BOT_TOKEN') 
bot = telebot.TeleBot(TOKEN)

# ... (qalan kod eynidir)

# 2. RENDER-DƏ OYAQ QALMAQ ÜÇÜN VEB SERVER (Flask)
app = Flask('')

@app.route('/')
def home():
    return "Homework Bot statusu: Oyaqdır və işləyir! 🚀"

def run():
    # Render avtomatik olaraq 'PORT' təyin edir, onu tutmalıyıq
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

# 3. BOTUN MƏNTİQİ (Ev Tapşırığı və Cədvəl)
data = {
    "tasks": [],
    "schedule": "Cədvəl hələ daxil edilməyib."
}

@bot.message_handler(commands=['start'])
def welcome(message):
    help_text = (
        "📚 *Ev Tapşırığı Edition* xoş gəldin!\n\n"
        "Komandalar:\n"
        "🔹 `Tapşırıq: [mətn]` - Yeni tapşırıq əlavə et\n"
        "🔹 `Tapşırıqlar` - Siyahını gör\n"
        "🔹 `Cədvəl: [mətn]` - Cədvəli yenilə\n"
        "🔹 `Cədvəl gör` - Dərs cədvəlinə bax"
    )
    bot.reply_to(message, help_text, parse_mode='Markdown')

@bot.message_handler(func=lambda m: True)
def handle_messages(message):
    text = message.text.lower()

    # Tapşırıq əlavə etmək
    if text.startswith("tapşırıq:"):
        task = message.text.split(":", 1)[1].strip()
        data["tasks"].append(task)
        bot.reply_to(message, "✅ Tapşırıq yaddaşa atıldı!")

    # Tapşırıqları görmək
    elif "tapşırıqlar" in text:
        if data["tasks"]:
            tasks_list = "\n".join([f"{i+1}. {t}" for i, t in enumerate(data["tasks"])])
            bot.send_message(message.chat.id, f"📝 *Sənin Tapşırıqların:*\n{tasks_list}", parse_mode='Markdown')
        else:
            bot.reply_to(message, "Hazırda heç bir tapşırığın yoxdur. İstirahət et! 😎")

    # Cədvəl yeniləmək
    elif text.startswith("cədvəl:"):
        data["schedule"] = message.text.split(":", 1)[1].strip()
        bot.reply_to(message, "📅 Cədvəl yeniləndi!")

    # Cədvələ baxmaq
    elif "cədvəl gör" in text:
        bot.send_message(message.chat.id, f"🗓 *Dərs Cədvəli:*\n{data['schedule']}", parse_mode='Markdown')

# 4. BOTU İŞƏ SALMAQ
if __name__ == "__main__":
    keep_alive() # Bu hissə oyaq qalmaq üçün 'spam' (ping) qəbul edir
    print("Bot işə düşdü...")
    bot.polling(none_stop=True)
