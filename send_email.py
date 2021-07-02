import smtplib, ssl, os

def send_email(message):
    port = 465
    server = 'smtp.gmail.com'
    sender_email = os.getenv('USER_EMAIL')
    password = os.getenv('USER_PASSWORD')
    receiver= os.getenv('RECEIVER_EMAIL')

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(server, port, context=context) as server:
        try:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver, message)
            print('message sent')
        except Exception as e:
            print(e)
            print('could not login or send the mail')

