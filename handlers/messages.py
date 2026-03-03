from telegram import Update
from telegram.ext import ContextTypes
from sessions import get_session, clear_session
from selenium_service import open_login_and_capture_captcha, perform_login

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text.strip()
    session = get_session(user_id)

    # STEP 1: REG NO
    if "reg_no" not in session:
        session["reg_no"] = text
        await update.message.reply_text("🔐 Please send your Password:")

    # STEP 2: PASSWORD
    elif "password" not in session:
        session["password"] = text
        await update.message.reply_text("⏳ Opening login page...")

        driver = open_login_and_capture_captcha()
        session["driver"] = driver

        await update.message.reply_photo(photo=open("captcha.png", "rb"))
        await update.message.reply_text("🧠 Please enter captcha shown above:")

    # STEP 3: CAPTCHA
    else:
        driver = session["driver"]
        success = perform_login(
            driver,
            session["reg_no"],
            session["password"],
            text
        )

        if success:
            await update.message.reply_text("✅ Login Successful!\nFetching Grade Card...")

            # Example: capture dashboard screenshot
            driver.save_screenshot("gradecard.png")
            await update.message.reply_photo(photo=open("gradecard.png", "rb"))

        else:
            await update.message.reply_text("❌ Login Failed. Try again.")

        driver.quit()
        clear_session(user_id)
