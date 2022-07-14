from telegram import ReplyKeyboardMarkup, Update, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, ConversationHandler

import sheet

sh = sheet.Sheet
new_slot = {}
del_slot = {}

key = "5534382664:AAGzSPk90NRvAgV80OYDdhSHfK4iN1s2VNA"

NAME, DAY, TIME, FIN = range(4)
NAME1, DAY1, TIME1, FIN1 = range(4)

#START
def start(update: Update, context: CallbackContext) -> None:
    user_name = update.message.from_user.name
    update.message.reply_text("Hello, {}!\nUse the following commands to:\n1./add the rehearsal\n2./delete the rehearsal\n3./list to view the empty slots".format(user_name))

#LIST
def get_list(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(sh.get_all_list())
    return ConversationHandler.END


# ADD
def add(update:Update, context: CallbackContext) -> None:
    reply_keyboard = [['Yes', 'No']]
    update.message.reply_text("Do you want to add the time slot? (Yes/No)",
    reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder='Yes/No?'
        ),)
    
    return NAME

def name(update:Update, context: CallbackContext) -> None:
    if update.message.text == 'Yes':
        update.message.reply_text('Enter your first and second name(in order)')
        return DAY
    else:
        update.message.reply_text('Reservation canceled')
        return ConversationHandler.END

def day(update:Update, context: CallbackContext) -> None:
    if sh.isListed(update.message.text) == False:
        update.message.reply_text("You don't have an access or you are banned")
        return ConversationHandler.END
    
    new_slot['name']= update.message.text

    reply_keyboard = [['Mon'], ['Tue'], ['Wed'], ['Thu'], ['Fri'], ['Sat'], ['Sun']]
    update.message.reply_text('Day?', reply_markup=ReplyKeyboardMarkup(
        reply_keyboard, one_time_keyboard=True,  input_field_placeholder='Day?'
    ))
    return TIME

def time(update:Update, context: CallbackContext) -> None:
    update.message.reply_text(sh.get_list_day(update.message.text))
    new_slot['day']= update.message.text
    reply_keyboard = [['9:00 - 10:00'], ['10:00 - 11:00'], ['11:00 - 12:00'], ['12:00 - 13:00'], ['13:00 - 14:00'], ['14:00 - 15:00'],
    ['15:00 - 16:00'], ['16:00 - 17:00'], ['17:00 - 18:00'], ['18:00 - 19:00'], ['19:00 - 20:00'], ['20:00 - 21:00'], ['21:00 - 22:00'], ['22:00 - 23:00']]
    update.message.reply_text('Select the time slot', reply_markup=ReplyKeyboardMarkup(
        reply_keyboard, one_time_keyboard=True, input_field_placeholder='Time?'
    ))
    return FIN

def fin(update: Update, context:CallbackContext) -> None:
    time = [['9:00 - 10:00'], ['10:00 - 11:00'], ['11:00 - 12:00'], ['12:00 - 13:00'], ['13:00 - 14:00'], ['14:00 - 15:00'],
    ['15:00 - 16:00'], ['16:00 - 17:00'], ['17:00 - 18:00'], ['18:00 - 19:00'], ['19:00 - 20:00'], ['20:00 - 21:00'], ['21:00 - 22:00'], ['22:00 - 23:00']]
    for i in time:
        if i[-1] == update.message.text:
            update.message.reply_text(sh.add(new_slot['name'], new_slot['day'], time.index(i) + 9))
    new_slot.clear()
    return ConversationHandler.END

def cancel_add(update:Update, context: CallbackContext) -> None:
    update.message.reply_text('Reservation canceled', reply_markup=ReplyKeyboardRemove())
    new_slot.clear()
    return ConversationHandler.END

#DELETE
def delete(update:Update, context:CallbackContext) -> None:
    reply_keyboard = [['Yes', 'No']]
    update.message.reply_text("Do you want to delete the time slot? (Yes/No)",
    reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder='Yes/No?'
        ),)

    return NAME1

def delete_name(update:Update, context:CallbackContext) -> None:
    if update.message.text == 'Yes':
        update.message.reply_text('Enter your first and second name(in order)')
        return DAY
    else:
        update.message.reply_text('Reservation canceled')
        return ConversationHandler.END

def delete_day(update:Update, context: CallbackContext) -> None:
    if sh.isListed(update.message.text) == False:
        update.message.reply_text("You don't have an access or you are banned")
        return ConversationHandler.END
    
    del_slot['name']= update.message.text

    reply_keyboard = [['Mon'], ['Tue'], ['Wed'], ['Thu'], ['Fri'], ['Sat'], ['Sun']]
    update.message.reply_text('Day?', reply_markup=ReplyKeyboardMarkup(
        reply_keyboard, one_time_keyboard=True,  input_field_placeholder='Day?'
    ))
    return TIME

def delete_time(update:Update, context: CallbackContext) -> None:
    update.message.reply_text(sh.get_list_day(update.message.text))
    del_slot['day']= update.message.text
    reply_keyboard = [['9:00 - 10:00'], ['10:00 - 11:00'], ['11:00 - 12:00'], ['12:00 - 13:00'], ['13:00 - 14:00'], ['14:00 - 15:00'],
    ['15:00 - 16:00'], ['16:00 - 17:00'], ['17:00 - 18:00'], ['18:00 - 19:00'], ['19:00 - 20:00'], ['20:00 - 21:00'], ['21:00 - 22:00'], ['22:00 - 23:00']]
    update.message.reply_text('Select the time slot', reply_markup=ReplyKeyboardMarkup(
        reply_keyboard, one_time_keyboard=True, input_field_placeholder='Time?'
    ))
    return FIN

def delete_fin(update: Update, context:CallbackContext) -> None:
    time = [['9:00 - 10:00'], ['10:00 - 11:00'], ['11:00 - 12:00'], ['12:00 - 13:00'], ['13:00 - 14:00'], ['14:00 - 15:00'],
    ['15:00 - 16:00'], ['16:00 - 17:00'], ['17:00 - 18:00'], ['18:00 - 19:00'], ['19:00 - 20:00'], ['20:00 - 21:00'], ['21:00 - 22:00'], ['22:00 - 23:00']]
    for i in time:
        if i[-1] == update.message.text:
            update.message.reply_text(sh.delete(del_slot['name'], del_slot['day'], time.index(i) + 9))
    del_slot.clear()
    return ConversationHandler.END

def cancel_delete(update:Update, context: CallbackContext) -> None:
    update.message.reply_text('Deletion canceled', reply_markup=ReplyKeyboardRemove())
    del_slot.clear()
    return ConversationHandler.END

    

def main():
    updater = Updater(key)
    dispatcher = updater.dispatcher

    add_conv = ConversationHandler(
        entry_points=[CommandHandler("add", add)],
        states={
            NAME: [MessageHandler(Filters.regex('^(Yes|No)$'), name)],
            DAY: [MessageHandler(Filters.text, day)],
            TIME: [MessageHandler(Filters.regex('^(Mon|Tue|Wed|Thu|Fri|Sat|Sun)$'), time)],
            FIN: [MessageHandler(Filters.all, fin)]
            },
        fallbacks=[CommandHandler('cancel', cancel_add)],
        conversation_timeout=300
    )
    del_conv = ConversationHandler(
        entry_points=[CommandHandler("delete", delete)],
        states={
            NAME1: [MessageHandler(Filters.regex('^(Yes|No)$'), delete_name)],
            DAY1: [MessageHandler(Filters.text, delete_day)],
            TIME1: [MessageHandler(Filters.regex('^(Mon|Tue|Wed|Thu|Fri|Sat|Sun)$'), delete_time)],
            FIN1: [MessageHandler(Filters.all, delete_fin)]
        },
        fallbacks=[CommandHandler('cancel', cancel_delete)],
        conversation_timeout=300
    )

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("list", get_list))
    dispatcher.add_handler(add_conv)
    dispatcher.add_handler(del_conv)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()