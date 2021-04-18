from telegram import Bot
from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext, ConversationHandler, CommandHandler
from conversations.parent_conv import PARENT, parent_conv
from conversations.teacher_conv import TEACHER, teacher_conv
from conversations.model import Model
import os
import logging
import pytest

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = os.environ.get('TOKEN')

Teacher = Model('teacher')
Parent = Model('parent')


def start(update: Update, context: CallbackContext):
    username = update.message.from_user.username

    if _is_teacher(username):
        Teacher.update(
            {"username": username},
            {"$set": {"chat_id": update.message.chat_id}}
        )
        context.bot.send_message(
            chat_id=update.message.chat_id,
            text="Вы успешно зарегистрированы"
        )
        return TEACHER

    for _ in Parent.find_all({"username": username}):
        Parent.update(
            {"username": username},
            {"$set": {"chat_id": update.message.chat_id}}
        )
        context.bot.send_message(
            chat_id=update.message.chat_id,
            text="Вы успешно зарегистрированы"
        )
        return PARENT


def _is_teacher(username):
    for _ in Teacher.find_all({"username": username}):
        return True
    return False


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def exit():
    pass


def main():
    # Teacher.insert_one({"username": "matvey22122"})
    # Parent.insert_one({"teacher_username": "matvey22122", "children_fio": "Иванов Иван Иванович", "is_attend": 0, "reason": "Не захотел"})
    # Parent.insert_one({"teacher_username": "matvey22122", "children_fio": "Иванов Иван Иванович", "is_attend": 1, "reason": "Не захотел"})
    # Parent.insert_one({"teacher_username": "matvey22122", "children_fio": "Иванов Иван Иванович", "is_attend": 2, "reason": "Не захотел"})

    bot = Bot(token=TOKEN)
    updater = Updater(bot=bot, use_context=True)
    dp = updater.dispatcher

    main_conversation = ConversationHandler(
        entry_points=[MessageHandler(Filters.text, start)],
        states={
            TEACHER: teacher_conv,
            PARENT: parent_conv
        },
        fallbacks=[CommandHandler('exit', exit)]
    )

    dp.add_handler(main_conversation)

    dp.add_error_handler(error)

    updater.start_polling()


if __name__ == '__main__':
    main()
