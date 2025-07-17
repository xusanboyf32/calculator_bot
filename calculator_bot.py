import requests
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

user_histories = {}

def calculate_math(expression):
    url = "https://math6.p.rapidapi.com/generate"
    payload = {"data": expression}
    headers = {
        "x-rapidapi-key": "681d33d17amsh5b06fddb725f4fap1f1a34jsnb2ed2c4e5dd6",
        "x-rapidapi-host": "math6.p.rapidapi.com",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        result = response.json()
        return result.get("result", "Hisoblashda xatolik!")
    except:
        return "Xatolik yuz berdi!"

def start(update, context):
    update.message.reply_text("Salom! Matematik ifoda yuboring (masalan: 2*(3+4)).\n\n"
                              "🧾 Tarixni ko‘rish uchun: /history")

def handle_message(update, context):
    user_id = update.message.from_user.id
    expression = update.message.text
    result = calculate_math(expression)

    if user_id not in user_histories:
        user_histories[user_id] = []
    user_histories[user_id].append(f"{expression} = {result}")

    update.message.reply_text(f"Natija: {result}")



def show_history(update, context):
    user_id = update.message.from_user.id
    history = user_histories.get(user_id, [])

    if history:
        oxirgi_tarix = history[-10:]  # oxirgi 10 ta amal
        matn = ""
        for amal in oxirgi_tarix:
            matn += f"\n{amal}\n" + "_" * 32 + "\n\n"
        update.message.reply_text(f"🧾 Hisoblash tarixi:\n{matn}")
    else:
        update.message.reply_text("Sizda hali hech qanday hisoblash yo‘q.")



def main():
    updater = Updater("", use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("history", show_history))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()








