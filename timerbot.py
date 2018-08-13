from telegram.ext import CommandHandler


def get_commands():
    commands = "Timer commands:\n/timer <seconds>\n/stoptimer\n"
    return commands


def add_handlers(dispatcher):
    timer_handler = CommandHandler("timer", timer, pass_args=True, pass_job_queue=True, pass_user_data=True)
    dispatcher.add_handler(timer_handler)

    stoptimer_handler = CommandHandler("stoptimer", stoptimer, pass_user_data=True)
    dispatcher.add_handler(stoptimer_handler)


def timer(bot, update, args, job_queue, user_data):
    chat_id = update.message.chat_id
    try:
        duration = int(args[0])
        if duration > 0:
            job = job_queue.run_once(alarm, when=duration, context=chat_id)
            user_data['job'] = job
            update.message.reply_text('Timer set.')
        else:
            update.message.reply_text("Time must be positive.")
    except (IndexError, ValueError):
        update.message.reply_text("Timer is not set, try again.")


def stoptimer(bot, update, user_data):
    if 'job' in user_data:
        job = user_data['job']
        job.schedule_removal()
        del user_data['job']
        update.message.reply_text('Timer stopped.')
    else:
        update.message.reply_text('No active timer.')


def alarm(bot, job):
    bot.send_message(job.context, text='Timer!!!')
