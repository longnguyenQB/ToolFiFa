from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import random
import re
import json
import email
import imaplib


def choice_reaction():
    list_reaction = ['Thích', 'Yêu thích', 'Thương thương']
    return random.choice(list_reaction)


def sleep_very_short():
    return time.sleep(random.choice([0.1, 0.2, 0.3, 0.4, 0.5, 0.6]))


def sleep_short():
    return time.sleep(random.choice(range(2, 5)))


def sleep_long():
    return time.sleep(random.choice(range(5, 10)))


def sleep_very_long():
    return time.sleep(random.choice(range(8, 20)))


def sleep_very_very_long():
    return time.sleep(random.choice(range(20, 60)))


# Vẽ frame message
def _one_frame(text):                 # text is supposed to be a list of lines
    lt = len(text[0])
    horz = '+' + '-'*lt + '+'         # Make the horizontal line +-------+
    result = [horz]                   # Top of the frame
    for line in text:
        result.append('|'+line+'|')  # Add the borders for each line
    result.append(horz)               # Bottom of the frame
    return result


def frame(text, repeat, thickness):
    text = [" %s " % text]*repeat       # add spaces and repeat as a list
    for i in range(thickness):
        text = _one_frame(text)       # draw one frame per iteration
    return '\n'.join(text)            # join lines


def open_txt(path):
    with open(path, 'r', encoding="utf8") as f:
        content = [word.split("\n")[0] for word in f]
    f.close()
    return content


def write_txt(path, content):
    with open(path, 'w', encoding="utf8") as f:
        for line in content:
            f.write(f"{line}\n")
    f.close()


def read_js(path):
    f = open(path, "r", encoding='utf-8')
    data = json.loads(f.read())
    return data


def write_js(data, path):
    with open(path, 'w', encoding='utf-8') as file:
        json.dump(data, file)


def gen_name(name_vn):
    anphabelt = 'abcdefghijklmnopqrstuvwxyz'
    number = '0123456789'
    name_anphabelt = ''
    name_number = ''
    for _ in range(random.randint(1, 6)):
        name_anphabelt += random.choice(anphabelt)
    for _ in range(random.randint(1, 4)):
        name_number += random.choice(number)
    name = name_vn + random.choice(
        ['_', '.']) + "fan" + random.choice(['_', '.']) + name_number
    return name


def gen_password():
    anphabelt = 'abcdefghijklmnopqrstuvwxyz'
    number = '0123456789'
    password_anphabelt = ''
    password_number = ''
    for _ in range(random.randint(4, 8)):
        password_anphabelt += random.choice(anphabelt)
        password_number += random.choice(number)
    return '@' + password_anphabelt + password_number


def get_code_email(EMAIL, PASSWORD):
    SERVER = 'outlook.office365.com'
    try:

        mail = imaplib.IMAP4_SSL(SERVER)
        mail.login(EMAIL, PASSWORD)
        x = mail.select('Inbox')  #readonly=True
        num = x[1][0].decode('utf-8')
        # from here you can start a loop of how many mails you want, if 10, then num-9 to num
        resp, lst = mail.fetch(num, '(RFC822)')
        body = lst[0][1]
        email_message = email.message_from_bytes(body)

        return email_message['Subject'][:6]
    except:
        return "Không đăng nhập được vào mail"
    

def get_data(path1, path2, path_save):
    data = open_txt(path=path1)
    name_vn = open_txt(path=path2)
    for i in range(len(data)):

        data[i] = random.choice(name_vn) + "|" + data[i] 
        
    write_txt(path=path_save, content=data)
