import telebot
from telebot import types
import random, time, urllib.parse
from datetime import datetime, timedelta
import threading

# --- 🔐 CONFIG ---
BOT_TOKEN = "8402941434:AAEBQABlDVtgbiVqZMNdAXuvWPkTE1HNvyw"
bot = telebot.TeleBot(BOT_TOKEN, parse_mode="Markdown")

OWNER_ID = 8188755760
REAL_UPI = "swatantrsingh42@okhdfcbank"

# --- DATA --- 
user_expiry = {}        
user_timer_started = {}
user_history = {}
user_payments = {}
user_game_id = {}      # 👈 1Win Game ID store
user_wait_msg = {}    # 👈 3 sec wait message id

# --- 🧠 SIGNAL GENERATOR (same as your Lifi) ---
def generate_signal_like_screenshot():
    r = random.random()
    if r < 0.55:
        return round(random.uniform(1.00, 1.30), 2)
    elif r < 0.80:
        return round(random.uniform(1.30, 2.50), 2)
    elif r < 0.99:
        return round(random.uniform(2.5, 9.0), 2)
    else:
        return round(random.uniform(6.0, 50.0), 2)

# --- 🕒 REAL-TIME TIMER ---
def start_realtime_timer(uid):
    while uid in user_expiry:
        left = int((user_expiry[uid] - datetime.now()).total_seconds())
        if left <= 0:
            break
        time.sleep(1)

    if uid in user_expiry:
        del user_expiry[uid]

    user_history.pop(uid, None)
    user_payments.pop(uid, None)
    user_timer_started.pop(uid, None)
    user_game_id.pop(uid, None)

    try:
        bot.send_message(uid, "❌ **Time Over!**\n🗑️ Sab kuch clear kar diya gaya hai.",
                         reply_markup=types.ReplyKeyboardRemove())
    except:
        pass

# --- 🏠 START ---
@bot.message_handler(commands=["start"])
def start(message):
    uid = message.chat.id

    if uid == OWNER_ID:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add("🚀 NEXT SIGNAL")
        bot.send_message(uid, "👑 **Admin Active**", reply_markup=markup)
        return

    if uid in user_expiry and datetime.now() < user_expiry[uid]:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add("🚀 NEXT SIGNAL")
        bot.send_message(uid, "✅ **VIP Active**", reply_markup=markup)
    else:
        markup = types.InlineKeyboardMarkup(row_width=2)
        plans = [
            ("₹2500 (15 Min)", "2500_6"),
            ("₹3500 (30 Min)", "3500_10"),
            ("₹4500 (35 Min)", "4500_15"),
            ("₹5500 (45 Min)", "5500_25"),
            ("₹6500 (60 Min)", "6500_30"),
        ]       
        for name, data in plans:
            markup.add(types.InlineKeyboardButton(name, callback_data=f"buy_{data}"))

        bot.send_message(uid, "🤖 **AVIATOR PREMIUM SIGNAL (LIFI)**", reply_markup=markup)

# --- 🚀 NEXT SIGNAL (2sec wait + auto delete wait msg) ---
@bot.message_handler(func=lambda m: m.text == "🚀 NEXT SIGNAL")
def next_signal(message):
    uid = message.chat.id

    if uid != OWNER_ID and (uid not in user_expiry or datetime.now() > user_expiry[uid]):
        bot.send_message(uid, "❌ Access Denied!")
        return

    if uid != OWNER_ID and not user_timer_started.get(uid, False):
        user_timer_started[uid] = True
        threading.Thread(target=start_realtime_timer, args=(uid,), daemon=True).start()

    wait_msg = bot.send_message(uid, "⏳ **Signal loading... 2 sec wait**")
    user_wait_msg[uid] = wait_msg.message_id

    time.sleep(2)

    try:
        bot.delete_message(uid, user_wait_msg.get(uid))
    except:
        pass

    now = datetime.now().strftime("%I:%M:%S %p")
    val = generate_signal_like_screenshot()

    left_sec = "∞"
    if uid in user_expiry:
        left_sec = int((user_expiry[uid] - datetime.now()).total_seconds())

    bot.send_message(
        uid,
        f"🚀 **SIGNAL: {val}x**\n"
        f"🎮 Game ID: `{user_game_id.get(uid, 'Not Set')}`\n"
        f"⏰ Time: `{now}`\n"
        f"⏳ Remaining: `{left_sec} sec`"
    )

# --- 💳 PAYMENT ---
@bot.callback_query_handler(func=lambda c: c.data.startswith("buy_"))
def handle_pay(call):
    _, amt, mins = call.data.split("_")
    upi_url = f"upi://pay?pa={REAL_UPI}&am={amt}&cu=INR"
    qr = f"https://api.qrserver.com/v1/create-qr-code/?size=900x900&data={urllib.parse.quote(upi_url)}"
    bot.send_photo(call.message.chat.id, qr,
                   caption=f"💳 **PAY ₹{amt} FOR {mins} MIN**\n\n12-digit UTR bhejo.")

# --- 💰 UTR VERIFY ---
@bot.message_handler(func=lambda m: m.text and m.text.isdigit() and len(m.text) == 12)
def verify(message):
    if message.chat.id == OWNER_ID:
        return

    markup = types.InlineKeyboardMarkup()
    options = [5, 9, 19, 28, 30, 48]
    for t in options:
        markup.add(types.InlineKeyboardButton(f"Approve {t} Min", callback_data=f"ok_{t}_{message.chat.id}"))
    markup.add(types.InlineKeyboardButton("❌ Reject", callback_data=f"no_{message.chat.id}"))

    bot.send_message(OWNER_ID, f"💰 **New UTR**\nUser: `{message.chat.id}`\nUTR: `{message.text}`",
                     reply_markup=markup)
    bot.send_message(message.chat.id, "⏳ Admin verify kar raha hai...")

# --- 🔘 ADMIN ACTION ---
@bot.callback_query_handler(func=lambda c: c.data.startswith(("ok_", "no_")))
def admin_action(call):
    data = call.data.split("_")
    bot.delete_message(call.message.chat.id, call.message.message_id)

    if data[0] == "no":
        target = int(data[1])
        bot.send_message(target, "❌ Payment Failed!")
    else:
        mins, target = int(data[1]), int(data[2])
        user_expiry[target] = datetime.now() + timedelta(minutes=mins)
        user_timer_started[target] = False

        bot.send_message(target, "🎮 **Apni 1Win Game ID bhejo** (sirf ID):")

# --- 🎮 GAME ID CAPTURE ---
@bot.message_handler(func=lambda m: m.text and m.text.isdigit() and 6 <= len(m.text) <= 12)
def save_game_id(message):
    uid = message.chat.id
    user_game_id[uid] = message.text
    bot.send_message(uid, "✅ Game ID save ho gayi.\n👉 Ab NEXT SIGNAL dabao.")

bot.infinity_polling()  
