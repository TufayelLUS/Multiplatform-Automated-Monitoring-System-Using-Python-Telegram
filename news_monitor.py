import requests
import threading
from time import sleep
import re
from bs4 import BeautifulSoup as bs
import sqlite3
import html
from urllib.parse import quote

# pip install requests bs4

recheck_delay = 300  # amount of time to wait between each recheck for new post


def sendMsg(msg):
    msg = quote(msg)
    key = ""  # telegram bot api key
    chat_id = ""  # telegram channel id
    msgApi = "https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}&parse_mode=HTML".format(
        key, chat_id, msg)
    try:
        # HTTP request to telegram API for message notification
        requests.get(msgApi).text
        print("Notified on telegram!")
    except:
        print("Failed to notify on telegram!")


def createTable():
    connection = sqlite3.connect("memory.db")
    try:
        cursor = connection.cursor()
        sql = """CREATE TABLE IF NOT EXISTS binance (
                id integer PRIMARY KEY,
                link text NOT NULL
        )
        """
        cursor.execute(sql)
        cursor = connection.cursor()
        sql = """CREATE TABLE IF NOT EXISTS bitmaxhelp (
                id integer PRIMARY KEY,
                link text NOT NULL
        )
        """
        cursor.execute(sql)
        cursor = connection.cursor()
        sql = """CREATE TABLE IF NOT EXISTS bitforex (
                id integer PRIMARY KEY,
                link text NOT NULL
        )
        """
        cursor.execute(sql)
        cursor = connection.cursor()
        sql = """CREATE TABLE IF NOT EXISTS kraken (
                id integer PRIMARY KEY,
                link text NOT NULL
        )
        """
        cursor.execute(sql)
    except Exception as e:
        print(str(e))
    finally:
        connection.commit()
        connection.close()


def isOldBinance(item):
    connection = sqlite3.connect("memory.db")
    try:
        cursor = connection.cursor()
        sql = """SELECT * FROM binance WHERE link = ?
        """
        cursor.execute(sql, (item, ))
        result = cursor.fetchall()
        if len(result) > 0:
            return True
        return False
    except Exception as e:
        print(str(e))
    finally:
        connection.close()


def insertToBinance(item):
    connection = sqlite3.connect("memory.db")
    try:
        cursor = connection.cursor()
        sql = """INSERT INTO binance VALUES(null, ?)
        """
        cursor.execute(sql, (item, ))
    except Exception as e:
        print(str(e))
    finally:
        connection.commit()
        connection.close()


def isOldBitMaxHelp(item):
    connection = sqlite3.connect("memory.db")
    try:
        cursor = connection.cursor()
        sql = """SELECT * FROM bitmaxhelp WHERE link = ?
        """
        cursor.execute(sql, (item, ))
        result = cursor.fetchall()
        if len(result) > 0:
            return True
        return False
    except Exception as e:
        print(str(e))
    finally:
        connection.close()


def insertToBitMaxHelp(item):
    connection = sqlite3.connect("memory.db")
    try:
        cursor = connection.cursor()
        sql = """INSERT INTO bitmaxhelp VALUES(null, ?)
        """
        cursor.execute(sql, (item, ))
    except Exception as e:
        print(str(e))
    finally:
        connection.commit()
        connection.close()


def isOldBitForex(item):
    connection = sqlite3.connect("memory.db")
    try:
        cursor = connection.cursor()
        sql = """SELECT * FROM bitforex WHERE link = ?
        """
        cursor.execute(sql, (item, ))
        result = cursor.fetchall()
        if len(result) > 0:
            return True
        return False
    except Exception as e:
        print(str(e))
    finally:
        connection.close()


def insertToBitForex(item):
    connection = sqlite3.connect("memory.db")
    try:
        cursor = connection.cursor()
        sql = """INSERT INTO bitforex VALUES(null, ?)
        """
        cursor.execute(sql, (item, ))
    except Exception as e:
        print(str(e))
    finally:
        connection.commit()
        connection.close()


def isOldKraken(item):
    connection = sqlite3.connect("memory.db")
    try:
        cursor = connection.cursor()
        sql = """SELECT * FROM kraken WHERE link = ?
        """
        cursor.execute(sql, (item, ))
        result = cursor.fetchall()
        if len(result) > 0:
            return True
        return False
    except Exception as e:
        print(str(e))
    finally:
        connection.close()


def insertToKraken(item):
    connection = sqlite3.connect("memory.db")
    try:
        cursor = connection.cursor()
        sql = """INSERT INTO kraken VALUES(null, ?)
        """
        cursor.execute(sql, (item, ))
    except Exception as e:
        print(str(e))
    finally:
        connection.commit()
        connection.close()


def binanceChecker():
    link = "https://www.binance.com/en/support/announcement/c-48?navId=48"
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36'
    }
    while True:
        print("Checking binance for new news ...")
        try:
            resp = requests.get(link, headers=headers).content
        except:
            print("Failed to open {}".format(link))
            continue
        soup = bs(resp, 'html.parser')
        news_list = soup.findAll('a', {'class': 'css-1ej4hfo'})
        msg = ""
        has_news = False
        for news in news_list[::-1]:
            if news.get('href') is not None:
                if isOldBinance(news.get('href')):
                    continue
                insertToBinance(news.get('href'))
                has_news = True
                msg += "Title: {}\nLink: {}\n".format(html.unescape(
                    news.text.strip()), "https://www.binance.com" + news.get('href'))
        if has_news:
            print(msg)
            sendMsg(msg)
        print("Binance checker going to sleep for {} seconds".format(recheck_delay))
        sleep(recheck_delay)


def bitMaxHelpChecker():
    link = "https://bitmaxhelp.zendesk.com/hc/en-us/sections/360003095033-New-Listing"
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36'
    }
    while True:
        print("Checking bitmaxhelp for new news ...")
        try:
            resp = requests.get(link, headers=headers).content
        except:
            print("Failed to open {}".format(link))
            continue
        soup = bs(resp, 'html.parser')
        news_list = soup.findAll('a', {'class': 'article-list-link'})
        msg = ""
        has_news = False
        for news in news_list[::-1]:
            if news.get('href') is not None:
                if isOldBitMaxHelp(news.get('href')):
                    continue
                insertToBitMaxHelp(news.get('href'))
                has_news = True
                msg += "Title: {}\nLink: {}\n".format(html.unescape(
                    news.text.strip()), "https://bitmaxhelp.zendesk.com" + news.get('href'))
        if has_news:
            print(msg)
            sendMsg(msg)
        print("Bitmaxhelp checker going to sleep for {} seconds".format(recheck_delay))
        sleep(recheck_delay)


def bitForexChecker():
    link = "https://support.bitforex.com/hc/en-us/sections/360001499772-New-Listings"
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9,bn;q=0.8',
        'cache-control': 'max-age=0',
        'dnt': '1',
        'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'cross-site',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
    }
    while True:
        print("Checking bitforex for new news ...")
        try:
            resp = requests.get(link, headers=headers).content
        except:
            print("Failed to open {}".format(link))
            continue
        soup = bs(resp, 'html.parser')
        news_list = soup.findAll('a', {'class': 'article-list-link'})
        msg = ""
        has_news = False
        for news in news_list[::-1]:
            if news.get('href') is not None:
                if isOldBitForex(news.get('href')):
                    continue
                insertToBitForex(news.get('href'))
                has_news = True
                msg += "Title: {}\nLink: {}\n".format(html.unescape(
                    news.text.strip()), "https://support.bitforex.com" + news.get('href'))
        if has_news:
            print(msg)
            sendMsg(msg)
        print("Bitforex checker going to sleep for {} seconds".format(recheck_delay))
        sleep(recheck_delay)


def krakenChecker():
    link = "https://blog.kraken.com"
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
    }
    while True:
        print("Checking kraken for new news ...")
        try:
            resp = requests.get(link, headers=headers).content
        except:
            print("Failed to open {}".format(link))
            continue
        soup = bs(resp, 'html.parser')
        news_list = soup.findAll('h1', {'class': 'entry-title'})
        msg = ""
        has_news = False
        for news in news_list[::-1]:
            if news.a.get('href') is not None:
                if isOldKraken(news.a.get('href')):
                    continue
                insertToKraken(news.a.get('href'))
                has_news = True
                msg += "Title: {}\nLink: {}\n".format(
                    html.unescape(news.a.text.strip()), news.a.get('href'))
        if has_news:
            print(msg)
            sendMsg(msg)
        print("Kraken checker going to sleep for {} seconds".format(recheck_delay))
        sleep(recheck_delay)


def createMonitorThreads():
    all_threads = []
    thread = threading.Thread(target=binanceChecker, args=())
    thread.daemon = True
    thread.start()
    all_threads.append(thread)
    thread = threading.Thread(target=bitMaxHelpChecker, args=())
    thread.daemon = True
    thread.start()
    all_threads.append(thread)
    thread = threading.Thread(target=bitForexChecker, args=())
    thread.daemon = True
    thread.start()
    all_threads.append(thread)
    thread = threading.Thread(target=krakenChecker, args=())
    thread.daemon = True
    thread.start()
    all_threads.append(thread)
    for item in all_threads:
        item.join()


if __name__ == "__main__":
    createTable()
    print("Program started ...")
    createMonitorThreads()
