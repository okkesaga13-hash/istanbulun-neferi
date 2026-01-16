import os
from telegram import Update, ChatPermissions
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from datetime import timedelta
import re

# BOT TOKEN
TOKEN = os.getenv("BOT_TOKEN")

# --------------------------
# Komutlar
# --------------------------

async def mute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.reply_to_message:
        await update.message.reply_text("❗ Susturmak için bir mesaja yanıt ver.")
        return

    user = update.message.reply_to_message.from_user
    chat_id = update.effective_chat.id

    try:
        await context.bot.restrict_chat_member(
            chat_id=chat_id,
            user_id=user.id,
            permissions=ChatPermissions(can_send_messages=False),
            until_date=timedelta(hours=2)  # 2 saat mute
        )

        await update.message.reply_text(
            f"🔇 {user.first_name} 2 saat susturuldu.\nİstanbul'un Neferi emrinde."
        )

    except Exception as e:
        await update.message.reply_text(f"❌ Yetkim yok veya hata oluştu: {e}")


# --------------------------
# Yeni katılanları karşılama
# --------------------------
async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for member in update.message.new_chat_members:
        await update.message.reply_text(
            f"👋 Hoş geldin {member.first_name}! İstanbul'un Neferi seni selamlıyor."
        )


# --------------------------
# Spam ve link engelleme
# --------------------------
async def filter_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    text = update.message.text.lower()

    # Link kontrolü
    if re.search(r"(http[s]?://|www\.)", text):
        try:
            await update.message.delete()
            await update.message.reply_text("❌ Link paylaşmak yasak!")
        except:
            pass

    # Basit küfür filtresi
    forbidden_words = ["siktir", "aq", "amk", "orospu", "mal", "salak"]
    if any(word in text for word in forbidden_words):
        try:
            await update.message.delete()
            await update.message.reply_text("❌ Küfür etmek yasak!")
        except:
            pass


# --------------------------
# BOT BAŞLATMA
# --------------------------
def main():
    application = ApplicationBuilder().token(TOKEN).build()

    # Komutlar
    application.add_handler(CommandHandler("mute", mute))

    # Yeni katılanları karşılama
    application.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome))

    # Spam ve küfür engelleme
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, filter_messages))

    print("🤖 İstanbul'un Neferi aktif...")
    application.run_polling()


if __name__ == "__main__":
    main()
