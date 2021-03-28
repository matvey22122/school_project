from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CallbackContext, MessageHandler, Filters
from .model import Model

PARENT = 2
Parent = Model('parent')


def yes(update: Update, context: CallbackContext):
    username = update.message.from_user.username
    Parent.update(
        {"username": username},
        {"$set": {"is_attend": 1, "reason": ""}}
    )
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text="Спасибо, ответ принят.",
    )


def no(update: Update, context: CallbackContext):
    username = update.message.from_user.username
    Parent.update(
        {"username": username},
        {"$set": {"is_attend": 0}}
    )
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text="Опишите в следующем сообщении причину.",
    )


def reason(update: Update, context: CallbackContext):
    username = update.message.from_user.username
    Parent.update(
        {"username": username},
        {"$set": {"reason": update.message.text}}
    )
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text="Спасибо, ответ принят. Если вы ошиблись и хотите исправить что-то, то отправьте заново.",
    )


parent_conv = [
    MessageHandler(Filters.regex('^Да$'), yes),
    MessageHandler(Filters.regex('^Нет$'), no),
    MessageHandler(Filters.text, reason),
]
