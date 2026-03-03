from telegram import Update
from telegram.ext import ContextTypes
from sessions import get_session

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    session = get_session(user_id)
    session.clear()

    await update.message.reply_text(
        "👋 Welcome to BEU Grade Card Bot\n\n"
        "Please send your Registration Number:"
    )
