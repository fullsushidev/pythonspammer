# -*- coding: utf-8 -*-
import csv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

SENDER_EMAIL = 'spamer@python.io'
SENDER_NAME = 'Python Spammer :)'
EMAIL_SUBJECT = f'Olá! Você tem um novo e-mail do {SENDER_NAME}'
# password = '@#!' # senha do email do remetente


def prepare_msg(recipient_name, recipient_email):
    """
    Prepara e retorna uma mensagem de e-mail
    """

    msg = MIMEMultipart('alternative')
    msg['From'] = f'{SENDER_NAME} <{SENDER_EMAIL}>'
    msg['To'] = recipient_email
    msg['Subject'] = EMAIL_SUBJECT
    text = '''
    Olá ''' +recipient_name+ ''', este é um texto básico no corpo do e-mail e sem formatação,
    caso o seu usuário abra esse e-mail em algum ~lugar~ sem suporte HTML.
    '''
    html = '''
    <h1>Olá ''' +recipient_name+ ''',</h1>
    <h4>este é um texto básico no corpo do e-mail e com formatação simples em HTML</h4>
    <p>Esse texto irá aparecer caso o usuáriocaso o seu usuário abra esse e-mail em algum ~lugar~ COM suporte HTML.</p>
    '''
    msg.attach(MIMEText(text, 'plain'))
    msg.attach(MIMEText(html, 'html'))
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    return msg


def send_mail(recipient_name, recipient_email):
    """
    Envia e-mail para o destinatário com email `recipient_email` e nome `recipient_name`    .
    """

    smtp = smtplib.SMTP('localhost', 1025)
    # smtp = smtplib.SMTP('smtp.gmail.com', 587)
    # smtp.starttls()
    # smtp.login(send_from, password)
    email_msg = prepare_msg(recipient_name, recipient_email)
    smtp.sendmail(SENDER_EMAIL, recipient_email, email_msg.as_string())
    smtp.close()


def process_file(filename):
    """
    Abre o csv indicado por `filename` em modo leitura e para cada linha,
    exeto a primeira (cabeçalho), extrai o nome e e-mail dos destinatários.
    Para cada conjunto de nome e e-mail encontrado, a função de envio de e-mail
    `send_mail` é executada.
    """

    with open(filename, 'r') as csv_file:
        users = csv.reader(csv_file, delimiter=',')
        next(users, None) # pulando cabeçalho do csv

        for name, email in users:
            print(name,email)
            send_mail(name, email)


if __name__ == '__main__':
    process_file('lista.csv')
