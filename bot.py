import sys
import time
import telepot
import os
import datetime

from selenium import webdriver

"""
Run with
$ python3.4 bot.py <token> <PTC username> <PTC password> <steps> <host> <port> <gmaps key>

"""

def handle(msg):
    flavor = telepot.flavor(msg)
    chat_id = msg['chat']['id']
    command = msg['text']
    sender = msg['from']
    msg_date = msg['date']
    actual_date = time.time()

    summary = telepot.glance(msg, flavor=flavor)

    if command.lower().startswith('/pokemap'):
        if command.count(' ') >= 1:
            # printing info
            print('Sender: ', sender)
            print('Command: ', command)
            print('Msg date: ', msg_date)
            print('Act date: ', actual_date)
            if msg_date+1 > actual_date:
                # saving the location into a variable
                locTemp = command.split(' ', 1)
                location = locTemp[1]
                # running the shell command
                os.system('python PokemonGo-Map-develop/runserver.py -a ptc -u %s -p %s -l "%s" -st %s -H %s -P %s >mapstd.txt 2>maperr.txt &' % (USER, PASS, location, STEP, HOST, PORT))
                # let the map load a minute
                bot.sendMessage(chat_id, 'Wait a minute...')
                time.sleep(60)
                # initializing the page
                driver = webdriver.PhantomJS()
                driver.set_window_size(1024, 1024)
                driver.get('http://%s:%s' % (HOST, PORT))
                # let the page load
                time.sleep(5)
                # save a screenshot
                driver.save_screenshot('loc.png')
                # kill the map
                os.system('pkill -f runserver.py')
                os.system('pkill -f node')
                os.system('pkill -f phantomjs')
                # send the screenshot
                bot.sendChatAction(chat_id, 'upload_photo')
                bot.sendPhoto(chat_id, open('loc.png', 'rb'), caption=location)
            else:
                bot.sendMessage(chat_id, 'I\'m now avaiable')
        else:
            bot.sendMessage(chat_id, 'Correct syntax is "/pokemap location"')

    elif command.lower().startswith('/start'):
        bot.sendMessage(chat_id, 'Hi!')

    elif command.lower().startswith('/help'):
        bot.sendMessage(chat_id,    'To get the map of a location with nearby Pokémon, just type\n' \
                                    '/pokemap followed by the desired location\n\n' \
                                    'Sources can be found here https://github.com/robbcocco/PokemonGo-Map-forTelegram', disable_web_page_preview=True)


TOKEN = sys.argv[1]  # get token from command-line

USER = sys.argv[2]
PASS = sys.argv[3]
STEP = sys.argv[4]
HOST = sys.argv[5]
PORT = sys.argv[6]
#GKEY = sys.argv[7]

bot = telepot.Bot(TOKEN)
bot.message_loop(handle)

# Keep the program running.
while 1:
    time.sleep(10)
