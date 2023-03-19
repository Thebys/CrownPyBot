import logging
import config
import multiprocessing
import events
from MachineBrain import MachineBrain
from telegram import Update
from telegram.ext import filters, ApplicationBuilder, ContextTypes, MessageHandler, CommandHandler


class CrownTelegramBot:
    """Crown Telegram Bot - it is used for direct control and status overview."""
    instance = None
    telegram_process = None
    enabled = False
    crown_telegram_queue = None

    def __new__(cls):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance

    def init_telegram_bot(self, CrownTelegramQueue):
        """Initialize the Crown Telegram Bot in background process."""
        logging.debug("TG - Initialization.")
        if len(config.TG_BOT_TOKEN) < 32:
            logging.debug(
                "TG - Telegram bot is disabled - entry valid API key to enable.")
            return
        else:
            self.enabled = True
            self.crown_telegram_queue = CrownTelegramQueue
            if self.telegram_process is None:
                self.telegram_process = multiprocessing.Process(
                    target=self.process_run_telegram_bot, args=(config.TG_BOT_TOKEN, self.crown_telegram_queue))
                self.telegram_process.start()
            logging.debug(
                "TG - Telegram bot should be running in background now.")

    def check_telegram_bot(self):
        """Check if the Telegram bot is still running."""
        if self.telegram_process is None:
            logging.debug("TG - Telegram bot is not running, restarting.")
            self.init_telegram_bot()
        elif not self.telegram_process.is_alive():
            logging.debug("TG - Telegram bot is not running, restarting.")
            self.init_telegram_bot()

    async def say(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        text_to_say = update.message.text.removeprefix("/say ")
        logging.debug(f"TG - Received command to say: {text_to_say}")
        event = events.Event(events.EventTypes.DIRECT_SPEECH, text_to_say)
        self.crown_telegram_queue.put(event, False)
        await context.bot.send_message(chat_id=update.effective_chat.id,  text=f"Will say: '{text_to_say}'")

    def process_run_telegram_bot(self, Token, Queue):
        '''Run the Telegram bot in a separate process, register handlers and start blocking polling.'''
        logging.debug("TG - Background process started.")
        application = ApplicationBuilder().token(Token).build()
        say_handler = CommandHandler('say', self.say)
        application.add_handler(say_handler)
        application.run_polling()
