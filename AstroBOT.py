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

    teclado = [["Un saludo al bot"], ["Contacto"+emoji.emojize(':v:',  use_aliases=True)], ["¿Y cómo estuvo su dia?", "¿Cómo hizo esto?"],  [
        "No hace nada", "Algo interesante"], ["Optical Character Recognition", "Chao"]]
    reply_markup = ReplyKeyboardMarkup(teclado, resize_keyboard=True)

    bot.sendMessage(chat_id= id_usuario, text= "¡Hola!"+" "+user.first_name+" (Si ocupás ayuda presiona \help)\n\nMarque una opción del teclado: ", reply_markup=reply_markup)

    #bot.sendMessage(chat_id=id_usuario, text= "Marque una opción del teclado: ", reply_markup=reply_markup)

    print("\n")

    
def aiuda(bot, update):
    
    print(update)

    id_usuario = update.message.chat_id

    bot.sendMessage(chat_id= id_usuario, text= "¡AIUDAAAAAAAAA!")

    bot.sendMessage(chat_id= id_usuario, text= "Siempre podés reiniciar el chat con el comando \start \n\nSi ocupás ayuda con otra vara escribime a @jfeng23")

    print("\n") 

    

def imagenes(bot, update):

    print(update)

    id_usuario = update.message.chat_id

    bot.sendMessage(chat_id= id_usuario, text= "Foto recibida")

    archivo = bot.getFile(update.message.photo[-1].file_id)

    archivo.download("imagen.jpg")

    texto1 = ocr_space("imagen.jpg")

    bot.sendMessage(chat_id= id_usuario, text= texto1)

    print("\n")

def ocr_space(filename, overlay=False, api_key='11a3e6dfb388957', language='spa'):

    # print(update)

    # Función para extraer el texto de una imagen
    # Cambiar "helloworld" por el id dado por OCR.space después de registrarse 

    payload = {'isOverlayRequired': overlay,
               'apikey': api_key,
               'language': language,
               }
    with open(filename, 'rb') as f:
        r = requests.post('https://api.ocr.space/parse/image',
                          files={filename: f},
                          data=payload,
                          )

    respuesta = json.loads(r.content.decode())
    print(respuesta)

    print("\n")

    try:
        texto = respuesta["ParsedResults"][0]["ParsedText"]
    except:
        texto = "No encontré texto"

    return texto

def saludo(bot, update):

    print(update)

    id_usuario = update.message.chat_id
    user = update.message.from_user

    bot.sendMessage(chat_id= id_usuario, text= "¡Saludos"+" "+user.first_name+"!"+emoji.emojize(':v:',  use_aliases=True))

    print("\n")


def dia(bot, update):

    print(update)

    id_usuario = update.message.chat_id

    bot.sendMessage(chat_id= id_usuario, text= emoji.emojize('Estuvo demasiado atareado :persevere:', use_aliases=True))

    print("\n")


def comoHizoEsto(bot, update):

    print(update)

    id_usuario = update.message.chat_id

    bot.sendMessage(chat_id= id_usuario, text= "De hecho que es vacilón, porque después de varios días de buscar en internet exhaustivamente, debuggear y ser un intenso con el mae que hizo el bot del TEC... Finalmente pude encontrar los errores :'D Pero más que todo fue por un taller que hiceron de bots y me emocioné haciendo algo bien cosi xD")

    print("\n")
    

def algo(bot, update):

    print(update)

    id_usuario = update.message.chat_id

    bot.sendMessage(chat_id= id_usuario, text= "\"No hace nada\" tiene un secreto...")

    global varCosi
    varCosi = 1

    print("\n")
     
    
varCosi = 0


def opcion(bot, update):

    print(update)

    id_usuario = update.message.chat_id

    if(varCosi == 0):

        bot.sendMessage(chat_id= id_usuario, text= "No hace nada :v")

    if(varCosi == 1):

        bot.sendMessage(chat_id= id_usuario, text= "La quiero mucho ❤️ y perdón por hacerla esperar ")

    print("\n")
        

def OCR(bot, update):

    print(update)

    id_usuario = update.message.chat_id 

    bot.sendMessage(chat_id= id_usuario, text= "Intente mandar una imagen que tenga texto para intentar sacarle el texto que tiene :)")
    
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

def button(bot, update):
    
   
    query = update.callback_query
    print("data: "+query.data)

    queryDat = query.data
    print("type "+type(queryDat))
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

updater.dispatcher.add_handler(MessageHandler(Filters.photo, imagenes))

updater.dispatcher.add_handler(RegexHandler("Un saludo al bot", saludo))
updater.dispatcher.add_handler(RegexHandler("Contacto",contact))
updater.dispatcher.add_handler(RegexHandler("¿Y cómo estuvo su dia?", dia))
updater.dispatcher.add_handler(RegexHandler("¿Cómo hizo esto?", comoHizoEsto))
updater.dispatcher.add_handler(RegexHandler("Algo interesante", algo))
updater.dispatcher.add_handler(RegexHandler("No hace nada", opcion))
updater.dispatcher.add_handler(RegexHandler("Optical Character Recognition", OCR))
updater.dispatcher.add_handler(RegexHandler("Contacto",contact))
updater.dispatcher.add_handler(RegexHandler("Chao", bye))

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
