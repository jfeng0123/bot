# -*- coding: UTF-8 -*-

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler, CallbackQueryHandler
from telegram import ReplyKeyboardMarkup, ReplyMarkup, ReplyKeyboardRemove, User, Update, InlineKeyboardButton, InlineKeyboardMarkup

import emoji

import sqlite3

import requests
import json

updater = Updater("512648855:AAEPuLnzGGNZ1evR2dm-ebZzrb5V7av7ZbE")

def listener(bot, update):
    id = update.message.chat_id
    user = update.message.from_user
    mensaje = update.message.text
 
    print("ID: " + user.first_name+ " "+ user.last_name+" ("+str(id)+")" + "; MENSAJE: " + mensaje)
    

def inicio(bot, update):

    print(update)
    
    id_usuario = update.message.chat_id
    user = update.message.from_user

    connection = sqlite3.connect('database.db')
    connection.row_factory = lambda cursor, row:row[0]
    cursor = connection.cursor()

    cursor.execute('SELECT ID FROM {table}'.format(table='WhiteList'))

    All_Names = cursor.fetchall()
    WhiteList = []
    for name in All_Names:
        print(name)
        WhiteList.append(name)
    print(WhiteList)

    if id_usuario in WhiteList:

        teclado = [["Un saludo al bot"], ["Contacto"+emoji.emojize(':v:',  use_aliases=True)], ["Chao"]]
        reply_markup = ReplyKeyboardMarkup(teclado, resize_keyboard=True)

        bot.sendMessage(chat_id=id_usuario, text="¡Hola!"+" "+user.first_name +
                    " (Si ocupás ayuda presiona /help)\n\nMarque una opción del teclado: ", reply_markup=reply_markup)
    
    else:
        teclado = []
        bot.sendMessage(chat_id=id_usuario, text="Sorry, unauthorized access denied for you: "+str(user.first_name))
        bot.sendMessage(parse_mode = 'HTML', chat_id= id_usuario, text= "Unless you have some secret <b>password</b> ...")

        ##password = "soyastroteco"

    print("\n")

    
def aiuda(bot, update):
    
    print(update)

    id_usuario = update.message.chat_id

    bot.sendMessage(chat_id= id_usuario, text= "¡AIUDAAAAAAAAA!")

    bot.sendMessage(chat_id= id_usuario, text= "Siempre podés reiniciar el chat con el comando /start \n\nSi ocupás ayuda con otra vara escribile a @jfeng23 o a @CdTrejos")

    print("\n") 


def saludo(bot, update):

    print(update)

    id_usuario = update.message.chat_id
    user = update.message.from_user

    bot.sendMessage(chat_id= id_usuario, text= "¡Saludos"+" "+user.first_name+"!"+emoji.emojize(':v:',  use_aliases=True))

    print("\n")
    

def contact(bot, update):


    id_usuario = update.message.chat_id

    bot.sendMessage(chat_id = id_usuario, text = "Aqui se encuentra los contactos")
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    cursor.execute('SELECT Name FROM {table}'.format(table='Contact'))
    All_Names = cursor.fetchall()
    options = []
    for name in All_Names:
        print(name)
        options.append([InlineKeyboardButton(name[0], callback_data=name[0])])

    keyboard = options
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Please choose:', reply_markup=reply_markup)

    print("\n")


def build_menu(buttons, n_cols, header_buttons=None, footer_buttons=None):

    bot.sendMessage(chat_id=id_usuario, text="¡1!")

    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]

    if header_buttons:
        menu.insert(0, header_buttons)

    if footer_buttons:
        menu.append(footer_buttons)

    bot.sendMessage(chat_id=id_usuario, text="¡2!")

    return menu


def password(bot, update):

    id_usuario = update.message.chat_id
    user = update.message.from_user
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('insert into WhiteList values ({ID})'.format(ID=id_usuario))
    connection.commit()
    connection.close()

    update.message.reply_text("Hello there 7u7 "+str(user.first_name)) ## Admitido en AstroTEC

    updater.dispatcher.remove_handler(RegexHandler("soyastroteco", password)) ## deja de escuchar la password

    inicio(bot,update) ## Remite al menú principal


def button(bot, update):
    
   
    query = update.callback_query
    print("data: "+query.data)

    queryDat = query.data
 #  print("type "+type(queryDat))
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('SELECT Contact,Expediente FROM Contact WHERE Name LIKE "{}"'.format((queryDat)))
    
    data = cursor.fetchone()
    contact = data[0]
    expediente = data[1]
    


    bot.edit_message_text(text="Contacto: \n    {cont} \nExpediente Medico: \n    {exp} \n".format(cont = contact, exp = expediente), chat_id=query.message.chat_id, message_id=query.message.message_id)


def bye(bot, update):

    print(update)

    #id_usuario = update.message.chat_id 

    update.message.reply_text(emoji.emojize('¡Pura vida! :punch:', use_aliases=True), reply_markup=ReplyKeyboardRemove())

    print("\n")

#Clasificadores

updater.dispatcher.add_handler(CommandHandler("start", inicio))
updater.dispatcher.add_handler(CommandHandler("help", aiuda))

updater.dispatcher.add_handler(RegexHandler("Un saludo al bot", saludo))
updater.dispatcher.add_handler(RegexHandler("Contacto",contact))
updater.dispatcher.add_handler(RegexHandler("Chao", bye))

updater.dispatcher.add_handler(RegexHandler("soyastroteco", password)) ## password listener


updater.dispatcher.add_handler(CallbackQueryHandler(button))
listener_handler = MessageHandler(Filters.text, listener)
updater.dispatcher.add_handler(listener_handler)

# https://www.webpagefx.com/tools/emoji-cheat-sheet/ 
# https://github.com/carpedm20/emoji/blob/master/emoji/unicode_codes.py
# -> Alias para los emojis

# http://bytelix.com/guias/crear-propio-bot-telegram/
# https://github.com/python-telegram-bot/python-telegram-bot/wiki/Code-snippets
# -> Ayudas para los bots

updater.start_polling()
updater.idle()
