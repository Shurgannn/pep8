import email
import smtplib
import imaplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class Email1:

    def __init__(self, my_login, password, message):
        self.my_login = my_login
        self.password = password
        self.message = message

    def recieve_mes(self):
        GMAIL_IMAP = 'imap.yandex.ru'
        header = None
        mail = imaplib.IMAP4_SSL(GMAIL_IMAP)
        mail.login(self.my_login, self.password)
        mail.list()
        mail.select("inbox")

        if header == '%':
            criterion = '(HEADER Subject "%s")'
        else:
            criterion = 'ALL'
        result, data = mail.uid('search', None, criterion)
        assert data[0], 'There are no letters with current header'
        latest_email_uid = data[0].split()[-1]
        result, data = mail.uid('fetch', latest_email_uid, '(RFC822)')
        raw_email = data[0][1]
        email_message = email.message_from_bytes(raw_email)
        print(email_message['To'])
        mail.logout()

    def send_mes(self):
        GMAIL_SMTP = 'smtp.yandex.ru'
        subject = 'subject'
        recipients = ['vasya@email.com', 'petya@email.com']
        msg = MIMEMultipart()
        msg['From'] = self.my_login
        msg['To'] = ', '.join(recipients)
        msg['Subject'] = subject
        msg.attach(MIMEText(self.message))
        ms = smtplib.SMTP(GMAIL_SMTP, 587)
        # identify ourselves to smtp gmail client
        ms.ehlo()
        # secure our email with tls encryption
        ms.starttls()
        # re-identify ourselves as an encrypted connection
        ms.ehlo()
        ms.login(self.my_login, self.password)
        ms.sendmail(self.my_login, recipients, msg.as_string())
        ms.quit()


if __name__ == '__main__':
    em = Email1('vasya@email.com', 'petya@email.com', 'Как дела')
    em.recieve_mes()
    em.send_mes()
