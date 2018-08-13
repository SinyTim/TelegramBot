from telegram import Bot
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import Filters

from database import database as db
import todobot
import timerbot


token = '---token---'


def help(bot, update):
    chat_id = update.message.chat_id
    commands = "Available commands:\n/help\n"
    todo_commands = todobot.get_commands()
    timer_commands = timerbot.get_commands()
    message = commands + todo_commands + timer_commands
    bot.send_message(chat_id=chat_id, text=message)


def text_callback(bot, update):
    todobot.text_callback(bot, update)


def add_handlers(dispatcher):
    start_handler = CommandHandler('start', help)
    dispatcher.add_handler(start_handler)

    help_handler = CommandHandler('help', help)
    dispatcher.add_handler(help_handler)

    todo_handler = MessageHandler(Filters.text, text_callback)
    dispatcher.add_handler(todo_handler)

    todobot.add_handlers(dispatcher)
    timerbot.add_handlers(dispatcher)


def main():
    db.create_table()

    updater = Updater(token=token)
    dispatcher = updater.dispatcher
    add_handlers(dispatcher)
    updater.start_polling()
    # updater.idle()


if __name__ == '__main__':
    main()
