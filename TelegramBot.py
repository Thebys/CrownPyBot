import logging
import config
import multiprocessing

from telegram import Update
from telegram.ext import filters, ApplicationBuilder, ContextTypes, MessageHandler, CommandHandler


class CrownTelegramBot:
    """Crown Telegram Bot - it is used for direct control and status overview."""
    instance = None
    telegram_process = None
    enabled = False

    def __new__(cls):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance

    def init_telegram_bot(self):
        """Initialize the Crown Telegram Bot in background process."""
        logging.debug("TG - Initialization.")
        if len(config.TG_BOT_TOKEN) < 32:
            logging.debug(
                "TG - Telegram bot is disabled - entry valid API key to enable.")
            return
        else:
            self.enabled = True
            if self.telegram_process is None:
                self.telegram_process = multiprocessing.Process(
                    target=self.process_run_telegram_bot, args=(config.TG_BOT_TOKEN,))
                self.telegram_process.start()
            logging.debug("TG - Telegram bot should be running in background now.")

    def check_telegram_bot(self):
        """Check if the Telegram bot is still running."""
        if self.telegram_process is None:
            logging.debug("TG - Telegram bot is not running, restarting.")
            self.init_telegram_bot()
        elif not self.telegram_process.is_alive():
            logging.debug("TG - Telegram bot is not running, restarting.")
            self.init_telegram_bot()

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

    async def echo(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

    def process_run_telegram_bot(self, Token):
        '''Run the Telegram bot in a separate process, register handlers and start blocking polling.'''
        logging.debug("TG - Background process started.")

        application = ApplicationBuilder().token(Token).build()

        echo_handler = MessageHandler(
            filters.TEXT & (~filters.COMMAND), self.echo)
        start_handler = CommandHandler('start', self.start)

        application.add_handler(start_handler)
        application.add_handler(echo_handler)
        application.run_polling()
