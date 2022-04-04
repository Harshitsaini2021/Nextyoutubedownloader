import telebot
from telebot import types
from pytube import YouTube  
from pytube.cli import on_progress
import urllib.request

import os,io


TOKEN = os.environ.get('TOKEN')

bot = telebot.TeleBot(token=TOKEN, parse_mode=None)


def makeMarkup(arr):
	markup = types.InlineKeyboardMarkup()
	for key,value in arr.items():
		markup.add(types.InlineKeyboardButton(text=value,callback_data=key))
	return markup


@bot.message_handler(commands=['start', 'help'])
def start(message):
	bot.reply_to(message, "Your most welcome on me. I am best YouTube videos downloader bot 😎. You can download any valid video by using me.")


@bot.callback_query_handler(func=lambda call:True)
def get(call):
	itag = call.data
	bot.edit_message_text(chat_id=call.message.chat.id,text='Yes, I am downloading file...', message_id=call.message.message_id)
	#yt.streams.get_by_itag(itag=itag).download()
	url = yt.streams.get_by_itag(itag=itag).url
	resp = urllib.request.urlopen(url)

        length = yt.streams.get_by_itag(itag=itag).filesize
	if length:
	    length = int(length)
	    blocksize = max(4096, length//100)
	else:
	    blocksize = 1000000 # just made something up
	
	print(length, blocksize)
	
	buf = io.BytesIO()
	size = 0
	while True:
	    buf1 = resp.read(blocksize)
	    if not buf1:
	        break
	    buf.write(buf1)
	    size += len(buf1)
	    if length:
                Percent = int((size / length)*100)
                bot.edit_message_text(chat_id=call.message.chat.id,text=f"Download: {Percent}% ",message_id=call.message.message_id)
	data = buf.getvalue()

	bot.send_video(caption=yt.title, thumb=yt.thumbnail_url, chat_id=call.message.chat.id,video=data,timeout=10000)
	bot.edit_message_text(chat_id=call.message.chat.id,text='Download complete', message_id=call.message.message_id)
	
@bot.message_handler(func=lambda m: True)
def download(message):
	chat_id = message.chat.id
	link = message.text
	try:
	    global yt
	    yt = YouTube(link,on_progress_callback=on_progress)  
	    print('Downloading...')
	    bot.send_message(chat_id=chat_id,text=f'Okk, I am downloading "{yt.title}" on my server')
	    stream = yt.streams.filter(type='video',progressive=True).order_by('resolution')
	    videos = {}
	    for i in stream:
	    	videos[i.itag]=str(str(i.mime_type).split('/')[1]+','+','+ i.resolution+','+ str(round(i.filesize_approx/1048576,2))+'MB') 
	    
	    bot.send_message(chat_id=chat_id,text="Downloaded 🙂",reply_markup=makeMarkup(videos),parse_mode='HTML')
	except Exception as e:
		print(e,"Connection Error") 
		bot.send_message(chat_id=chat_id,text="Sorry I can't recognize you , you said '%s'" % message.text) 


bot.infinity_polling()



   
   
