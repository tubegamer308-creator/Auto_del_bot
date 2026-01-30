import os
import asyncio
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    ContextTypes,
    filters
)

TOKEN = os.environ.get("BOT_TOKEN")
DELETE_AFTER = 86400  # 24 hours

async def is_admin(context, chat_id, user_id):
    admins = await context.bot.get_chat_administrators(chat_id)
    return any(admin.user.id == user_id for admin in admins)

async def auto_delete_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    if not msg:
        return

    chat_id = msg.chat.id
    user_id = msg.from_user.id

    # Admin check
    if await is_admin(context, chat_id, user_id):
        return  # Admin messages stay

    async def delayed_delete():
        await asyncio.sleep(DELETE_AFTER)
        try:
            await context.bot.delete_message(chat_id, msg.message_id)
        except:
            pass

    context.application.create_task(delayed_delete())

# --- App ---
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(
    MessageHandler(
        filters.TEXT
        | filters.PHOTO
        | filters.VIDEO
        | filters.STICKER
        | filters.ANIMATION,
        auto_delete_handler
    )
)

app.run_polling()
