from random import choice, shuffle
from telegram.ext import *
from telegram import ReplyKeyboardMarkup

my_persistence = PicklePersistence(filename='.data')


updater = Updater(token="YOUR TOKEN", persistence=my_persistence, use_context=True)

dispatcher = updater.dispatcher

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")
    
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

def pull(update, context):
    # add one to the total number of pulls
    if "pulls" not in context.user_data:
        context.user_data["pulls"] = 1
    else:
        context.user_data["pulls"] += 1

    username = update.message.from_user.username
    if "score" not in context.user_data:
        context.user_data["score"] = 100
    if context.user_data["score"] <= 1: # if the user doesn't have any money
        update.message.reply_text("You don't have enough credit")
        return
    context.user_data["score"] -= 2
    emojis = "🍌🍒🎱🍇🎁"
    result = choice(emojis) + choice(emojis) + choice(emojis)
    update.message.reply_text(result)
    if len(set(result)) == 1: # all three are the same
        if "jackpots" not in context.user_data:
            context.user_data["jackpots"] = 1
        else:
            context.user_data["jackpots"] += 1
        context.user_data["score"] += 100
        update.message.reply_text("Congrats, JACKPOT! your score: " + str(context.user_data["score"]))
    elif len(set(result)) == 2: # two of them are the same
        context.user_data["score"] += 1
        update.message.reply_text("Try again! your score: " + str(context.user_data["score"]))
    else:
        update.message.reply_text("Try again! your score: " + str(context.user_data["score"]))

pull_handler = CommandHandler('pull', pull)
dispatcher.add_handler(pull_handler)

def stat(update, context):
    if "pulls" in context.user_data:
        pulls = context.user_data["pulls"]
    else:
        update.message.reply_text("You have never played!")
        return
    if "jackpots" in context.user_data:
        jackpots = context.user_data["jackpots"]
    else:
        jackpots = 0
    update.message.reply_text("You have pulled the slot-machine lever " + str(pulls) + " times")
    if jackpots == 0:
        update.message.reply_text("You are a very unlucky person!")
    else:
        update.message.reply_text(f"{jackpots / pulls * 100: .2f}" + "% of them where jackpots")
stat_handler = CommandHandler('stat', stat)
dispatcher.add_handler(stat_handler)

def flip(update, context):
    if "players" in context.chat_data:
        context.chat_data["players"] += [update.message.from_user.full_name]
    else:
        context.chat_data["players"] = [update.message.from_user.full_name]
    if len(context.chat_data["players"]) == 2:
        r = choice([0, 1])
        update.message.reply_text(context.chat_data["players"][r] + " has won and " + context.chat_data["players"][1 - r] + " lost!")
        context.chat_data["players"] = []
flip_handler = CommandHandler('flip', flip)
dispatcher.add_handler(flip_handler)

def message(update, context):
    if update.message.text.find("bet") != -1:
        update.message.reply_text("betting is bad!")

message_handler = MessageHandler(Filters.text & (~Filters.command), message)
dispatcher.add_handler(message_handler)


def sticker(update, context):
    update.message.reply_text("that's an ugly sticker")

sticker_handler = MessageHandler(Filters.sticker, sticker)x
dispatcher.add_handler(sticker_handler)

updater.start_polling()