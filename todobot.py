from telegram.ext import CommandHandler
from telegram import ReplyKeyboardMarkup

from database import database as db


def get_commands():
    commands = "ToDo commands:\n/todo <task>\n/done\n/todolist\n"
    return commands


def text_callback(bot, update):
    chat_id = update.message.chat_id
    text = update.message.text
    items = db.get_items(chat_id)
    if text in items:
        db.delete_item(text, chat_id)
        send_todo_list(bot, chat_id)


def add_handlers(dispatcher):
    todo_handler = CommandHandler('todo', todo, pass_args=True)
    dispatcher.add_handler(todo_handler)

    done_handler = CommandHandler('done', done)
    dispatcher.add_handler(done_handler)

    todolist_handler = CommandHandler('todolist', todo_list)
    dispatcher.add_handler(todolist_handler)


def todo(bot, update, args):
    chat_id = update.message.chat_id
    text = ' '.join(args)
    if text != '':
        db.add_item(text, chat_id)
        send_todo_list(bot, chat_id)
    else:
        update.message.reply_text("Empty task, try again.")


def done(bot, update):
    chat_id = update.message.chat_id
    items = db.get_items(chat_id)
    if items:
        send_done_keyboard(bot, chat_id, items)
    else:
        bot.send_message(chat_id=chat_id, text="There are no tasks.")


def todo_list(bot, update):
    chat_id = update.message.chat_id
    send_todo_list(bot, chat_id)


def send_todo_list(bot, chat_id):
    items = db.get_items(chat_id)
    message = "ToDo list:\n>" + "\n>".join(items)
    bot.send_message(chat_id=chat_id, text=message)


def send_done_keyboard(bot, chat_id, items):
    keys = [[item] for item in items]
    reply_markup = ReplyKeyboardMarkup(keys, one_time_keyboard=True)
    bot.send_message(chat_id=chat_id, text="Select the task to delete.", reply_markup=reply_markup)
