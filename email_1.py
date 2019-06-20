import email
import smtplib
import imaplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class Email_1:

    def __init__(self):
        self.GMAIL_IMAP = 'imap.yandex.ru'
        self.GMAIL_SMTP = 'smtp.yandex.ru'
        self.my_login = 'vasya@email.com'
        self.password = 'qwerty'
        self.subject = 'Subject'
        self.recipients = ['vasya@email.com', 'petya@email.com']
        self.message = 'Message'
        self.header = None

    def recieve_mes(self):
        mail = imaplib.IMAP4_SSL(self.GMAIL_IMAP)
        mail.login(self.my_login, self.password)
        mail.list()
        mail.select("inbox")

        if self.header == '%':
            criterion = '(HEADER Subject "%s")'
        else:
            criterion = 'ALL'
        # criterion = '(HEADER Subject "%s")'
        # criterion = 'ALL'
        # criterion = '(HEADER Subject "%s")' % header if header else 'ALL'
        result, data = mail.uid('search', None, criterion)
        assert data[0], 'There are no letters with current header'
        latest_email_uid = data[0].split()[-1]
        result, data = mail.uid('fetch', latest_email_uid, '(RFC822)')
        raw_email = data[0][1]
        email_message = email.message_from_bytes(raw_email)
        # print(email_message)
        mail.logout()

    def send_mes(self):
        msg = MIMEMultipart()
        msg['From'] = self.my_login
        msg['To'] = ', '.join(self.recipients)
        msg['Subject'] = self.subject
        msg.attach(MIMEText(self.message))
        ms = smtplib.SMTP(self.GMAIL_SMTP, 587)
        # identify ourselves to smtp gmail client
        ms.ehlo()
        # secure our email with tls encryption
        ms.starttls()
        # re-identify ourselves as an encrypted connection
        ms.ehlo()
        ms.login(self.my_login, self.password)
        ms.sendmail(self.my_login, self.recipients, msg.as_string())
        ms.quit()


em = Email_1()
em.recieve_mes()
em.send_mes()
