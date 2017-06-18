import os
import telebot
from telebot import types
from vagalume import lyrics
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

TELEGRAMAPI = os.environ.get("TELEGRAM_API")
VAGALUMEAPI = os.environ.get("VAGALUME_API")

bot = telebot.TeleBot(TELEGRAMAPI)
token_vagalume = (VAGALUMEAPI)

class Object(object):
  pass

music = Object()
user = Object()

def bot_message(kind='error'):
  if kind == 'error':
    bot.send_message(user.id, 'Ops, algo deu errado.  Digite /start e tente novamente')
  if kind == 'notfound':
    bot.send_message(user.id,'Música e/ou artista não encontrado. Digite /start e tente novamente')
  if kind == 'start':
    bot.send_message(user.id, 'Digite /start para começar novamente')
  if kind == 'startremovemarkup':
    markup = types.ReplyKeyboardRemove()
    bot.send_message(user.id, 'Digite /start para começar novamente', reply_markup=markup)

@bot.message_handler(commands=['help']) 
def send_help(message):
  bot.reply_to(message, "Olá " + str(message.from_user.first_name) +
    '''\nPara utilizar o Letter2Music você precisa seguir esses passos:
    \n1- Digitar /start caso queira iniciar o bot;
    \n2- Pesquise conforme as informações forem solicitadas (Artista e Música).''')

@bot.message_handler(commands=['start']) 
def send_start(message):
  user.first_name = message.from_user.first_name
  user.id = message.from_user.id

  bot.send_message(user.id, 'Olá ' + user.first_name + '\nDigite o nome d@ Artista/Banda que deseja procurar:')
  bot.register_next_step_handler(message, send_artist)


def send_artist(message):
  try:
    music.artist = message.text
    if message.text != "/start" and message.text != "/help":
    	bot.send_message(user.id, 'Qual musica d@ ' + music.artist + ' você deseja procurar?')
    	bot.register_next_step_handler(message, send_song)
  except:
    bot_message()

def send_song(message):
  try:
  	if message.text != "/start" and message.text != "/help":
	    music.song = message.text
	    result = lyrics.find(music.artist, music.song)
	    if result.is_not_found():
	      bot_message('notfound')
	    else:
	      bot.send_message(user.id, result.song.lyric)
	      music.translation = result.get_translation_to('pt-br')
	      if music.translation:
	        markup = telebot.types.ReplyKeyboardMarkup()
	        translateButton = telebot.types.KeyboardButton('Traduzir')
	        closeButton = telebot.types.KeyboardButton('Cancelar')
	        markup.row(translateButton)
	        markup.row(closeButton)
	        bot.send_message(user.id, "Deseja traduzir?", reply_markup=markup)
	        bot.register_next_step_handler(message, show_translate)
	      else:
	        bot_message('start')
  except:
    bot_message()

def show_translate(message):
  if (message.text == 'Traduzir'):
    bot.send_message(user.id, music.translation.lyric)
  bot_message('startremovemarkup')

bot.polling()