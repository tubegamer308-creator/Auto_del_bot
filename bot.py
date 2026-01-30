import os
import asyncio
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    MessageHandler,
    filters
)

TOKEN = os.environ.get("BOT_TOKEN")

async def auto_delete(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    user = message.from_user

    # admin হলে skip
    admins = await context.bot.get_chat_administrators(message.chat_id)
    admin_ids = [admin.user.id for admin in admins]

    if user.id in admin_ids:
        return

    # 24 ঘণ্টা পরে delete
    await asyncio.sleep(86400)
    try:
        await message.delete()
    except:
        pass

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(
        MessageHandler(
            filters.PHOTO | filters.VIDEO | filters.TEXT | filters.Sticker.ALL | filters.ANIMATION,
            auto_delete
        )
    )

    app.run_polling()

if __name__ == "__main__":
    main()
