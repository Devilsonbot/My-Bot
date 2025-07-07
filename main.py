#!/usr/bin/env python
# pyright: reportUnusedVariable=false, reportGeneralTypeIssues=false

import logging
from telegram import __version__ as TG_VER

try:
  from telegram import __version_info__
except ImportError:
  __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
  raise RuntimeError(
      f"This example is not compatible with your current PTB version {TG_VER}. To view the "
      f"{TG_VER} version of this example, "
      f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html")

from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from PIL import Image, ImageDraw, ImageFont

# ✅ Your bot token directly inserted here
my_bot_token = "8011684873:AAGtg608p3kGR0TcvUV63VtwcrzEwjJDnJk"

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


# Handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
  user = update.effective_user
  await update.message.reply_html(
      rf"Hi {user.mention_html()}!",
      reply_markup=ForceReply(selective=True),
  )


async def help_command(update: Update,
                       context: ContextTypes.DEFAULT_TYPE) -> None:
  await update.message.reply_text("Help!")


async def stylize(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
  user_message = update.message.text
  if user_message is None:
    await update.message.reply_text("Please send an image to stylize.")
    return

  img = Image.new('RGB', (500, 200), color=(73, 109, 137))
  d = ImageDraw.Draw(img)
  fnt = ImageFont.load_default()
  d.text((50, 90), user_message, font=fnt, fill=(255, 255, 0))

  img.save('styled_text.png')
  with open('styled_text.png', 'rb') as photo:
    await update.message.reply_photo(photo=photo)


def main() -> None:
  application = Application.builder().token(my_bot_token).build()
  application.add_handler(CommandHandler("start", start))
  application.add_handler(CommandHandler("help", help_command))
  application.add_handler(
      MessageHandler(filters.TEXT & ~filters.COMMAND, stylize))
  application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
  main()
