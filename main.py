import telebot
import wikipedia
import re
import sqlite3


bot = telebot.TeleBot('5398325648:AAF9u7Xw9bju31xOqzJeILFbrDrsDA_H0hk')
wikipedia.set_lang("ru")


def getdefinition(word):
    con = sqlite3.connect('db.sqlite3')
    cur = con.cursor()
    result = cur.execute(f"""SELECT def FROM defs WHERE word = '{word}'""").fetchall()
    if not result:
        return None
    else:
        return result[0][0]


def getwiki(s):
    try:
        ny = wikipedia.page(s)
        wikitext = ny.content[:1000]
        wikimas = wikitext.split('.')
        wikimas = wikimas[:-1]
        wikitext2 = ''
        for x in wikimas:
            if not('==' in x):
                if(len((x.strip())) > 3):
                    wikitext2=wikitext2+x+'.'
            else:
                break
        wikitext2=re.sub('\([^()]*\)', '', wikitext2)
        wikitext2=re.sub('\([^()]*\)', '', wikitext2)
        wikitext2=re.sub('\{[^\{\}]*\}', '', wikitext2)
        # Возвращаем текстовую строку
        return wikitext2
    except Exception as e:
        return 'Нет информации об этом'


@bot.message_handler(commands=["start"])
def start(m, res=False):
    bot.send_message(m.chat.id, 'Отправьте мне любое слово, и я найду его значение')
@bot.message_handler(content_types=["text"])
def handle_text(message):
    if getdefinition(message.text) != None:
        send = getdefinition(message.text)
    else:
        send = getwiki(message.text)
    bot.send_message(message.chat.id, send)
bot.polling(none_stop=True, interval=0)
