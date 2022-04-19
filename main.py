from product import Product
import sqlite3 as sl
import urllib
from urllib import request
import json
import re


GREETINGS = ['hello', 'hey', 'hi', 'howdy']
FAREWELLS = ['goodbye', 'bye', 'thanks for helping', 'farewell', 'see you']
PRODUCT_ENQUIRIES = ['do you have', 'do you have any', 'can you recommend', 'do you sell']


def get_recommendation(question):
    answer = "I'm sorry, i didn't understand your question. Type !help for a list of helpful commands"
    for prod in get_products():
        if prod.name in question:
            if prod.isStocked():
                if prod.stock > 10:
                    answer = 'We have plenty of ' + prod.name + 's in stock.'
                else:
                    answer = "We are running low on " + prod.name + "s! Hurry up, and get yours now!"

                answer += ' Here is a list of our best sellers:\n'
                for link in str.split(prod.links):
                    answer += link + '\n'
            else:
                answer = prod.name + 's are unfortunately not in stock'
            break
    return answer


def send_report(unknown_question):
    con = sl.connect('bewhaosbot.db')
    sql = 'INSERT INTO NOTIFICATIONS (question) values(?)'
    data = [(unknown_question)]
    with con:
        con.execute(sql, data)
    return


def get_response(question):
    if any(map(question.__contains__, GREETINGS)):
        answer = 'Hello! What can i help you with?'
    elif question == '!help':
        answer = 'You can ask me about all of our products, and i can tell you about the weather in your city\nAsk away!'
    elif any(map(question.__contains__, FAREWELLS)):
        answer = 'Bye bye, have a nice day!'
    elif any(map(question.__contains__, PRODUCT_ENQUIRIES)):
        answer = get_recommendation(question)
    elif 'weather' in question:
        answer = get_weather()
    else:
        answer = "I'm sorry, i didn't understand your question. Type !help for a list of helpful commands"
        #send_report(question)
    return answer


def add_product(name, stock, links):
    con = sl.connect('bewhaosbot.db')
    sql = 'INSERT INTO PRODUCTS (name, stock, links) values(?,?,?)'
    data = (name, stock, links)
    with con:
        con.execute(sql, data)


def get_products():
    products = []
    con = sl.connect('bewhaosbot.db')
    with con:
        data = con.execute("SELECT * FROM PRODUCTS")
        for row in data:
            products.append(Product(row[0], row[1], row[2]))
    return products


def get_greetings():
    con = sl.connect('bewhaosbot.db')
    with con:
        data = con.execute("SELECT PHRASES FROM RESPONSES WHERE CATEGORY = 'greetings'")
        for row in data:
            greetings = row
    greetings = [s.replace(",", "") for s in greetings]
    return str.split(greetings[0])


def get_inquieries():
    con = sl.connect('bewhaosbot.db')
    with con:
        data = con.execute("SELECT PHRASES FROM RESPONSES WHERE CATEGORY = 'product_inquiries'")
        for row in data:
            inquiries = row
    stripped = [s.strip() for s in inquiries]
    return str.split(stripped[0], ",")


def get_farewells():
    farewells = []
    con = sl.connect('bewhaosbot.db')
    with con:
        data = con.execute("SELECT PHRASES FROM RESPONSES WHERE CATEGORY = 'farewells'")
        for row in data:
            farewells = row
    farewells = [s.replace(",", "") for s in farewells]
    return str.split(farewells[0])


def get_notifications():
    farewells = []
    con = sl.connect('bewhaosbot.db')
    with con:
        data = con.execute("SELECT * FROM NOTIFICATIONS")
        for row in data:
            farewells = row
    farewells = [s.replace(",", "") for s in farewells]
    return str.split(farewells[0])


def get_ip():
    url = 'http://checkip.dyndns.com/'
    data = request.urlopen(url).read()
    ip = data[-29:-16].decode('utf-8')
    return str.strip(ip)


def get_location():
    url = f'http://ipinfo.io/{get_ip()}/json'
    response = request.urlopen(url)
    data = json.load(response)
    city = data['city']
    return city


def get_weather():
    api_key = str('b190a0605344cc4f3af08d0dd473dd25')
    city = get_location()
    response = request.urlopen(f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric')
    data = json.load(response)
    temp = str(data['main']['temp'])
    answer = f'The temperature in {city} is {temp}C. '
    if float(temp) > 15:
        answer += 'What a lovely day!'
    else:
        answer += 'Better put on a jacket!'
    return answer


def bot_startup():
    return 'Hello and welcome to Bewhaos!'


if __name__ == '__main__':
    print(get_response('!help'))

