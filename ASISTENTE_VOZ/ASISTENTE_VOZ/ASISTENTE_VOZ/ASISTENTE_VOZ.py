import speech_recognition as sr
import pyttsx3
import webbrowser
import wikipedia
import datetime
import smtplib
import pywhatkit
import cv2

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


recognizer = sr.Recognizer()
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()


def get_command():
    with sr.Microphone() as source:
        print("Escuchando...")
        audio = recognizer.listen(source)

        try:
            command = recognizer.recognize_google(audio, language="es-ES")
            print(f"Comando detectado: {command}")
            return command.lower()
        except sr.UnknownValueError:
            speak("Lo siento, no entendí el comando.")
            return None
        except sr.RequestError as e:
            print(f"Error en la solicitud de reconocimiento de voz; {e}")
            return None


def take_photo():
    speak("Preparate para tomar una foto")
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    filename = "photo.jpg"
    cv2.imwrite(filename, frame)
    speak("¡Foto tomada con éxito!")
    cap.release()
    return filename


 
def send_email(to, subject, body):
    try:
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()

       
        email_address = "correo@gmail.com"
        email_password = "Contraseña"

        server.login(email_address, email_password)

        
        message = MIMEMultipart()
        message['From'] = email_address
        message['To'] = to
        message['Subject'] = subject

       
        message.attach(MIMEText(body, 'plain'))

       
        server.sendmail(email_address, to, message.as_string())

        
        server.quit()

        speak("Correo electrónico enviado correctamente.")
    except Exception as e:
        speak(f"No se pudo enviar el correo electrónico. Error: {str(e)}")
    


def main():
    speak("Hola, soy tu asistente virtual. ¿En qué puedo ayudarte?")

    while True:
        command = get_command()

        if command:
            if "nombre" in command:
                speak("Me llamo Asistente Virtual.")
            elif "reproducir vídeo" in command:
                speak("Ingresando a YouTube.")
                webbrowser.open("https://www.youtube.com/")
            elif "hora actual" in command:
                now = datetime.datetime.now()
                speak(f"La hora actual es {now.hour} horas y {now.minute} minutos.")
            elif "buscar en wikipedia" in command:
                speak("¿Qué tema te gustaría buscar en Wikipedia?")
                query = get_command()
                wikipedia.set_lang("es")  # Configura el idioma a español
                result = wikipedia.summary(query, sentences=2)
                speak(f"Según Wikipedia, {result}")
            elif "abrir google" in command:
                speak("Abriendo Google.")
                webbrowser.open("https://www.google.com/")
            elif "enviar correo" in command:
                speak("¿A quién le gustaría enviar el correo?")
                to = get_command()
                speak(f"¿Cuál es el asunto del correo para {to}?")
                subject = get_command()
                speak(f"Por favor, dicta el contenido del correo.")
                body = get_command()
                
                send_email(to, subject, body)

            elif "tomar foto" in command:
                filename = take_photo()
                speak("¡foto tomada con exito!")
            elif "salir" in command:
                speak("Hasta luego. ¡Que tengas un buen día!")
                break
            else:
                speak("Comando no reconocido.")

if __name__ == "__main__":
    main()

