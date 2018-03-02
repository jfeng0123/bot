from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, User, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler, CallbackQueryHandler
import requests
import json

updater = Updater("468841366:AAGKTrEggcwACcglDlw6Zuj98KzsMq5Kqck")

def inicio(bot, update):

    updater = Updater("468841366:AAGKTrEggcwACcglDlw6Zuj98KzsMq5Kqck")
    user = update.message.from_user

    whiteList = [334384720] ## Personas permitidas en el chat
    print(update) ## Imprime el status actual del usuario cuando se conecta al bot

    id_usuario = update.message.chat_id

    bot.sendMessage(chat_id= id_usuario, text= "¡Hola!")

    bot.sendMessage(chat_id= id_usuario, text= "Este es su ID: " + str(id_usuario)) ## ID_USUARIO

    if id_usuario not in whiteList: ## isOnList() ## Quitar el 'not' para que funcione como debe 

        with  open("/Users/zekrom/Desktop/base.txt", "r") as file:

            array = []

            for line in file:
                array.append(line)
        print(array)

        option = []
        for name in array:
            print (name)
            option.append([InlineKeyboardButton(name, callback_data=name)])

        keyboard = option
    ##    keyboard = [ [InlineKeyboardButton("Option 1", callback_data='1')],
    ##                 [InlineKeyboardButton("Option 2", callback_data='2')],
    ##
    ##                [InlineKeyboardButton("Option 3", callback_data='3')]] 

        reply_markup = InlineKeyboardMarkup(keyboard)

        update.message.reply_text('Please choose:', reply_markup=reply_markup)

    else: #!IsOnList()

        bot.sendMessage(chat_id= id_usuario, text= "Sorry, unauthorized access denied for you: "+str(user.first_name))
        bot.sendMessage(parse_mode = 'HTML', chat_id= id_usuario, text= "Unless you have some secret <b>password</b> ...")

        ##password = "soyastroteco"

        updater.dispatcher.add_handler(RegexHandler("soyastroteco", password)) ## Escucha la contraseña
        
def password(bot, update):

    user = update.message.from_user

    update.message.reply_text("Hello there 7u7 "+str(user.first_name))

    updater.dispatcher.remove_handler(RegexHandler("soyastroteco", done))

                         
def button(bot, update):
    
    query = update.callback_query

    bot.edit_message_text(text="Selected option: {}".format(query.data), chat_id=query.message.chat_id, message_id=query.message.message_id)

def done(bot, update):

    user = update.message.from_user

    update.message.reply_text("Ya ha sido agregado men ("+str(user.first_name)+")")

    
#Clasificadores

updater.dispatcher.add_handler(CommandHandler("start", inicio))

updater.dispatcher.add_handler(CallbackQueryHandler(button))

updater.dispatcher.add_handler(RegexHandler("soyastroteco", password))

updater.start_polling()
updater.idle()
