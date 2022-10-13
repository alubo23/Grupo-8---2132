from email.message import EmailMessage
import smtplib

def Correo(usuario, email_destino, codigo):
    remitente = "equipo_g8@outlook.com"
    destinatario = email_destino
    mensaje = usuario + ", bienvenido estas a solo un paso de ser parte de LBPH. \n\nIngresa el siguiente código para activar tu cuenta: \n\n"+codigo
    email = EmailMessage()
    email["To"] = destinatario
    email["Subject"] = "Codigo de Activacion"
    email.set_content(mensaje)
    smtp = smtplib.SMTP("smtp-mail.outlook.com", port=587)
    smtp.starttls()
    smtp.login(remitente, "centermail8")
    smtp.sendmail(remitente, destinatario, email.as_string())
    smtp.quit()
    
def RecuperarContraseña(email_destino): 
    remitente = "equipo_g8@outlook.com"
    destinatario = email_destino
    mensaje = "Para recuperar su contraseña ingrese al siguiente enlace: \n http://127.0.0.1:5000/nueva-contra"
    email = EmailMessage()
    email["From"] = remitente
    email["To"] = destinatario
    email["Subject"] = "Recuperación de Contraseña"
    email.set_content(mensaje)
    smtp = smtplib.SMTP("smtp-mail.outlook.com", port=587)
    smtp.starttls()
    smtp.login(remitente, "centermail8")
    smtp.sendmail(remitente, destinatario, email.as_string())
    smtp.quit()
    
def Notificacion(Usuario, email_destino): 
    remitente = "equipo_g8@outlook.com"
    destinatario = email_destino
    mensaje = Usuario + ", te ha enviado un nuevo mensaje"
    email = EmailMessage()
    email["From"] = remitente
    email["To"] = destinatario
    email["Subject"] = "¡Nuevo mensaje"
    email.set_content(mensaje)
    smtp = smtplib.SMTP("smtp-mail.outlook.com", port=587)
    smtp.starttls()
    smtp.login(remitente, "centermail8")
    smtp.sendmail(remitente, destinatario, email.as_string())
    smtp.quit()


    