from telegram import Update, ChatPermissions
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from datetime import timedelta

TOKEN = "8280413003:AAF5O0RkCB5MXGBAdOJvc8Xbl5PvX8_Lh3g"

async def mute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        await update.message.reply_text("❗ Susturmak için bir mesaja yanıt ver.")
        return

    user = update.message.reply_to_message.from_user
    chat_id = update.effective_chat.id

    try:
        await context.bot.restrict_chat_member(
            chat_id=chat_id,
            user_id=user.id,
            permissions=ChatPermissions(can_send_messages=False),
            until_date=timedelta(hours=2)
        )
        await update.message.reply_text(
            f"🔇 {user.first_name} 2 saat susturuldu.\nİstanbul’un Neferi emrinde."
        )
    except:
        await update.message.reply_text("❌ Yetkim yok veya hata oluştu.")

app = ApplicationBuilder().token(8280413003:AAF5O0RkCB5MXGBAdOJvc8Xbl5PvX8_Lh3g).build()
app.add_handler(CommandHandler("mute", mute))

print("🤖 İstanbul'un Neferi aktif...")
app.run_polling()
