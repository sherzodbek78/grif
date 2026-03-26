from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)

# ================== SOZLAMALAR ==================

BOT_TOKEN = "7292095010:AAFkTHN2P249CNkKTknYcUxbxAJqj9bQ2R4"

# Majburiy TELEGRAM kanallar (ID bilan — ishonchli)
CHANNELS = [
    {"id": "-1003440082304", "link": "https://t.me/+zdEKo4sH1qY2Nzcy"},
]

# Instagram (tekshiruvsiz)
INSTAGRAM_LINK = "https://https://www.instagram.com/kinolar_filmlar12?igsh=N2dvcm9jMmxyOHdn/username/"

# ================== KINO BAZASI (file_id bilan TEZ) ==================

movies = {
    "1": {
        "title": "tili",
        "year": "ozbek",
        "rating": "",
        "plot": "nomi: Qirol sher",
        "video":"https://t.me/kunfu_pand/297"  # <-- file_id
    },
    "181": {
        "title": "tili",
        "year": "ozbek",
        "rating": "",
        "plot": "nomi: chaqmoq makvin",
        "video": "https://t.me/chaqmoq_makvin4/5"  # <-- file_id
    }
}

# ================== YORDAMCHI FUNKSIYALAR ==================

async def is_subscribed_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    for ch in CHANNELS:
        try:
            member = await context.bot.get_chat_member(ch["id"], user_id)
            if member.status == "left":
                return False
        except Exception as e:
            print("SUB CHECK ERROR:", e)
            return False
    return True


def subscribe_keyboard():
    buttons = []

    # Telegram kanallar
    for i, ch in enumerate(CHANNELS, start=1):
        buttons.append([
            InlineKeyboardButton(f"📢 {i}-kanalga obuna", url=ch["link"])
        ])

    # Instagram (tekshiruvsiz)
    buttons.append([
        InlineKeyboardButton(f"📢 {i}-kanalga obuna", url=INSTAGRAM_LINK)
    ])

    # Tekshirish
    buttons.append([
        InlineKeyboardButton("✅ Tekshirish", callback_data="check_sub")
    ])

    return InlineKeyboardMarkup(buttons)

# ================== HANDLERLAR ==================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_subscribed_all(update, context):
        await update.message.reply_text(
            "🚫 Botdan foydalanish uchun barcha Telegram kanallarga obuna bo‘ling!\n\n",
            "📢 Telegram kanallar – majburiy\n"
                       "📸 Instagram – ixtiyoriy\n\n"
                "obuna bo'lgach *tekshirish* tugmasini bosing",

        reply_markup=subscribe_keyboard()
        )
        return

    await update.message.reply_text(
        "🎬 Xush kelibsiz!\nKino kodini yuboring"
    )


async def check_sub_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    if await is_subscribed_all(update, context):
        await query.message.edit_text(
            "✅ Obuna tasdiqlandi!\n\n🎬 Endi kino kodini yuboring"
        )
        await query.answer()
    else:
        await query.answer(
            "❌ Hali barcha Telegram kanallarga obuna bo‘lmagansiz!",
            show_alert=True
        )


async def get_movie(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_subscribed_all(update, context):
        await update.message.reply_text(
            "🚫 Avval barcha Telegram kanallarga obuna bo‘ling!",
            reply_markup=subscribe_keyboard()
        )
        return

    code = update.message.text.strip().upper()
    if code in movies:
        m = movies[code]
        info = (
            f"🎥 {m['title']} ({m['year']})\n"
            f"📖 {m['plot']}"
        )
        await update.message.reply_text(info)

        # TEZ yuborish (file_id)
        await update.message.reply_video(
            video=m["video"],
            supports_streaming=True
        )
    else:
        await update.message.reply_text("❌ Bunday kino kodi topilmadi.")

# ================== MAIN ==================
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(check_sub_callback, pattern="^check_sub$"))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, get_movie))

    print("🤖 Bot ishga tushdi...")
    app.run_polling()


if __name__ == "__main__":
    main()