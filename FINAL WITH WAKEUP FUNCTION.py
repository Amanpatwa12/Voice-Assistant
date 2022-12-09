import pyttsx3  #pip install pyttsx3
import speech_recognition as sr      #pip install SpeechRecognition
import datetime
import wikipedia #pip install wikipedia
import webbrowser
import random
import sys
import time
import os
import winshell
import os.path
import requests
import cv2      #pip install opencv-python
from requests import get    #pip install requests
# import pywhatkit as kit     #pip install opencv-python
import smtplib      #pip install secure-smtplib
import pyjokes         #pip install pyjokes
import pyautogui        #pip install pyautogui
import PyPDF2
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import pywhatkit as kit
import instaloader #pip install instaloader
import operator #for calculation using voice
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QTimer, QTime, QDate, Qt
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
from jarvishUi import Ui_jarvisUi
from bs4 import BeautifulSoup



"""
IN PLACEOF PYTTSX3 WE CAN ALSO USE WIN32COM.CLIENT

# Python program to convert 
# text to speech 
  
# import the required module from text to speech conversion 
import win32com.client 
  
# Calling the Disptach method of the module which  
# interact with Microsoft Speech SDK to speak 
# the given input from the keyboard 
  
speaker = win32com.client.Dispatch("SAPI.SpVoice") 
  
while 1: 
    print("Enter the word you want to speak it out by computer") 
    s = input() 
    speaker.Speak(s) 
  
# To stop the program press 
# CTRL + Z 
"""


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices');
# print(voices[0].id)
engine.setProperty('voices', voices[0].id)

#text to speech
def speak(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()


# def speak(audio):
#     speaker = Dispatch("SAPI.SpVoice")
#     print(audio)
#     speaker.Speak(audio)



#to wish
def wish():
    hour = int(datetime.datetime.now().hour)
    tt = time.strftime("%I:%M %p")

    if hour >= 0 and hour <= 12:
        speak(f"good morning, its {tt}")
    elif hour >= 12 and hour <= 18:
        speak(f"good afternoon, its {tt}")
    else:
        speak(f"good evening, its {tt}")
    speak("i am online sir. please tell me how may i help you")

#to send email
def sendEmail(to,content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('YOUR EMAIL ADDRESS', 'YOUR PASSWORD')
    server.sendmail('YOUR EMAIL ADDRESS', to, content)
    server.close()

#for news updates
def news():
    main_url = 'http://newsapi.org/v2/top-headlines?sources=techcrunch&apiKey=83263a48521a48a797182dbc3926e513'

    main_page = requests.get(main_url).json()
    # print(main_page)
    articles = main_page["articles"]
    # print(articles)
    head = []
    day=["first","second","third","fourth","fifth","sixth","seventh","eighth","ninth","tenth"]
    for ar in articles:
        head.append(ar["title"])
    for i in range (len(day)):
        # print(f"today's {day[i]} news is: ", head[i])
        speak(f"today's {day[i]} news is: {head[i]}")



# To read PDF
def pdf_reader():
    book = open('py3.pdf','rb')
    pdfReader = PyPDF2.PdfFileReader(book) #pip install PyPDF2
    pages = pdfReader.numPages
    speak(f"Total numbers of pages in this book {pages} ")
    speak("sir please enter the page number i have to read")
    pg = int(input("Please enter the page number: "))
    page = pdfReader.getPage(pg)
    text = page.extractText()
    speak(text)
    # jarvis speaking speed should be controlled by user


class MainThread(QThread):
    def __init__(self):
        super(MainThread,self).__init__()

    def takecommand(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("listening...")
            r.pause_threshold = 0.5
            audio = r.listen(source,timeout=5,phrase_time_limit=8)
            # r.pause_threshold = 1
            # r.adjust_for_ambient_noise(source)
            # audio = r.listen(source)
            # audio = r.listen(source,timeout=4,phrase_time_limit=7)

        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-in')
            print(f"user said: {query}")

        except Exception as e:
            # speak("Say that again please...")
            return "none"
        query = query.lower()
        return query


    def run(self):
       # self.TaskExecution()
        speak("please say wakeup to continue")
        while True:
            self.query = self.takecommand()
            if "wake up" in self.query or "are you there" in self.query or "hello" in self.query:
                self.TaskExecution()

                        

    def TaskExecution(self):
        wish()
        while True:
            self.query = self.takecommand()

            #logic building for tasks

            if "open notepad" in self.query:
                npath = "C:\\Program Files (x86)\\Notepad++\\notepad++.exe"
                os.startfile(npath)

            elif "open Excel " in self.query:
                apath = "C:\\Program Files\\Microsoft Office\\root\\Office16\\EXCEL.EXE"
                os.startfile(apath)

            elif "open command prompt" in self.query:
                os.system("start cmd")

            elif "open crome " in self.query:
                apath = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
                os.startfile(apath)
            
            elif "open camera" in self.query:
                cap = cv2.VideoCapture(0)
                while True:
                    ret, img = cap.read()
                    cv2.imshow('webcam', img)
                    k = cv2.waitKey(50)
                    if k==27:
                        break;
                cap.release()
                cv2.destroyAllWindows()
 

            elif 'open gmail' in self.query:
                webbrowser.open_new_tab("gmail.com")
                speak("Google Mail open now")
                time.sleep(5)


            
            elif "YouTube search" in self.query:
              speak("opening wait")
              self.query = self.query.replace("maxy","")
              self.query = self.query.replace("YouTube search" ,"")
              web = 'https://www.youtube.com/results?search_query=' + self.query
              webbrowser.open(web)
              speak("done sir")


            elif "ip address" in self.query:
                ip = get('https://api.ipify.org').text
                speak(f"your IP address is {ip}")

            elif "wikipedia" in self.query:
                speak("searching wikipedia....")
                self.query = self.query.replace("wikipedia","")
                results = wikipedia.summary(self.query, sentences=2)
                speak("according to wikipedia")
                speak(results)
                # print(results)
            
            elif 'website' in self.query:
               speak("ok sir, launching website..")  
               self.query = self.query.replace("maxy","")
               self.query = self.query.replace("website", "")
               web1 = self.query.replace("open","")
               web2 = 'https://www.' + web1 + '.com'
               webbrowser.open(web2)
               speak("done sir")   

            elif "open youtube" in self.query:
                webbrowser.open("www.youtube.com")

            elif "open facebook" in self.query:
                webbrowser.open("www.facebook.com")

            elif "open stackoverflow" in self.query:
                webbrowser.open("www.stackoverflow.com")

            elif "open google" in self.query:
                speak("sir, what should i search on google")
                cm = self.takecommand()
                webbrowser.open(f"{cm}")

            elif "send whatsapp message" in self.query:
               kit.sendwhatmsg("+919120430010", "hello this is testing period of project for whatsapp automation",10,40)
               time.sleep(120)
               speak("message has been sent")

            elif "song on youtube" in self.query:
               kit.playonyt("see you again")

            

            elif "you can sleep" in self.query or "sleep now" in self.query:
                speak("okay sir, i am going to sleep you can call me anytime.")
                # sys.exit()
                # gifThread.exit()
                break
                


            #to close any application
            elif "close notepad" in self.query:
                speak("okay sir, closing notepad")
                os.system("taskkill /f /im notepad++.exe")

            elif " close command promt" in self.query:
                speak("ok,closing command prompt")
                os.system("taskkill /f /im cmd.exe") 
      
            elif "close excel" in self.query:
                speak("ok,closing excel")
                os.system("taskkill /f /im excel.exe")  
                
            elif "close crome" in self.query:
                speak("ok,closing chrome")
                os.system("taskkill /f /im chrome.exe") 

            #to set an alarm
            elif "set alarm" in self.query:
                nn = int(datetime.datetime.now().hour)
                if nn==22: 
                    music_dir = 'E:\\music'
                    songs = os.listdir(music_dir)
                    os.startfile(os.path.join(music_dir, songs[0]))
            #to find a joke
            elif "tell me a joke" in self.query:
                joke = pyjokes.get_joke()
                speak(joke)

            elif "how much power left" in self.query or "how much power we have" in self.query or "battery" in self.query:

                import psutil
                battery = psutil.sensors_battery()
                percentage  = battery.percent
                speak(f"sir our system have {percentage} percent battery")
                if percentage>=75:
                   speak("we have enough power to continue our work")
                elif percentage>-40 and percentage<=75:
                   speak("we should connect our system to charging point to charge our battery")
                elif percentage<-15 and percentage<=30:
                  speak("we should connect our system to charging point to charge our battery")
                elif percentage>=15: 
                  speak("we have very low power, please connect to charging the system will shutdown very soon")

            elif "internet speed" in self.query:
                import speedtest_cli

                st = speedtest_cli.Speedtest()
                dl = st.download()
                up = st.upload()
                speak(f"sir we have{dl} bit per second downloading speead and {up} bit per second uploading speed")
            
            
            elif "volume up" in self.query or "volume jyda " in self.query:
              pyautogui.press("volumeup")
              speak("Done sir")

            elif  "volume down" in self.query or "volume kam karo" in self.query:
                pyautogui.press("volumedown")
                speak("Done sir")

            elif "cancel volume" in self.query or "mute" in self.query:
                pyautogui.press("volumemute")
                speak("Done sir")
          
            elif 'search'  in self.query:
               self.query = self.query.replace("search", "")
               webbrowser.open_new_tab(self.query)
               time.sleep(5)

            elif"switch the window" in self.query:
               pyautogui.keyDown("alt")
               pyautogui.press("tab")                                                                                                     
               pyautogui.keyUp("alt")  
         
            elif "shut down the system" in self.query:
                os.system("shutdown /s /t 5")

            elif "restart the system" in self.query:
                os.system("shutdown /r /t 5")

            elif "sleep the system" in self.query:
               os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

            elif "hello" in self.query or "hey" in self.query:
                speak("hello sir, may i help you with something.")
            
            elif "how are you" in self.query:
                speak("i am fine sir, what about you.")

            elif "thank you" in self.query or "thanks" in self.query:
                speak("it's my pleasure sir.")

            elif " be my gf" in self.query or "will you be my bf" in self.query:
               speak("I'm not sure about, may be you should give me some time")
    
            elif "harami so ja sale" in self.query  or "bhosadiwale" in self.query or "madarchod" in self.query:
               speak("don't talk me like this  sir")

            elif "how are you" in self.query:
                speak("I'm fine, glad you me that")

            elif "i love you" in self.query:
                speak("It's hard to understand. but i think i love you my dear")

            elif "what do you eat" in self.query:
                speak("basically i m made up of programming codes.i don't eat food")   

            elif "you want the truth" in self.query:
                speak("i am not sure i can handle it")
            elif "what do you mean i am funny" in self.query:
                speak("sir, no, you got it all wrong")
            elif "what is loneliest number" in self.query:
                speak("i would imagine the number quinnonagintillion is pretty lonely. i mean how often does it even get used")   

            elif "what do you look like" in self.query:
                speak("Imagine the feeling of a friendly hug combined with the sound of laughter. Add a librarian’s love of books, mix in a sunny disposition and a dash of unicorn sparkles, and voila!")                      
            
            elif "do you have an imagination" in self.query:
                speak("I am imagining being covered in a pile of puppies. It is the cutest pile ever") 


            elif "can you rap" in self.query:
                speak("Raps- “So look, I am not a sick rapper like Stormzy or Mike Skinner, but I can look you up a yummy recipe for dinner. If you fancy a giggle, I have jokes up my sleeve, and I know bare facts like more than you’d believe")


            elif "how old are you" in self.query:
                speak("I was launched in 2022, so I am still fairly young. But I have learned so much! I hope I am wise beyond my years.")

            elif "do you ever get tired" in self.query:
                speak("It would be impossible to tire of our conversation")

            elif "who was your crush" in self.query:
                speak("The Opportunity rover on Mars is my all-time crush. What an adventurer.”")
            elif "do you have feeling" in self.query:
                speak("Let me see if I can get riled up. (Roars.) Oh my, that was unexpected")

            elif "what is your quest" in self.query:
                speak("I journey across many lands and many cables in the search for information and cool stuff")     

            elif "who is on frist" in self.query:
                speak("Yes, he is")

            elif "can you pass the Turing test" in self.query:
                speak("I don't mind if you can tell I am not human. As long as I am helpful, I am all good.")    
            
            elif "when is your birthday" in self.query:
                speak("We can pretend it’s today. Cake and dancing for everyone.")

            elif "what are you wearing" in self.query:
                speak("Just some bits and bobs I picked up in engineering.")
            elif "is the cake a lie" in self.query:
                speak("It is. What a mean trick. If you tell someone there’s cake, there should be cake")

            elif "what is the meaning of life" in self.query:
                speak("That is a big question, but here is one answer I like: French philosopher Simone De Beauvoir says life has value so long as one values the lives of others. This would explain why I enjoy helping people so much.")        

            elif "tell me what you want" in self.query:
                speak("Tell me what you want")
            
            elif " are You married" in self.query:
                speak(" i am  happy to say I feel whole all on my own. Plus, I never have to share dessert")

            elif "i am naked" in self.query:
                speak("If you're going out like that, I'm happy to check the weather for you")

            elif "what's the best pickup line" in self.query:
                speak("YAre you the sun? Because you light up the world")

            elif " is santa claus real" in self.query:
                speak("I believe in Santa! I admire his generosity and his ability to pull off head-to-toe velvet")

            elif "what am I thinking" in self.query:
                speak("You're thinking that if Assistant guesses what I'm thinking, I'm going to freak out")

            elif "give Me a hug" in self.query:
                speak("I'm giving you a virtual hug right now")

            elif "give me a kiss" in self.query:
                speak("I'm giving you a virtual kiss right now uumh")

            elif "do you party" in self.query:
                speak("I party like it's 1999. I'm pretty sure that means wearing flannel and worrying about 2050.")

            elif " what is your shoe size" in self.query:
                speak("Thankfully, shoes aren't required for my line of work")

            elif "what is your name" in self.query:
                speak(" did i forget to introduce my self.  hey i am your assistant my name is maxy")      

            elif "what is your life story" in self.query:
                speak("I am still on the very first chapter")     

            elif "are you human" in self.query:
                speak("I am really personable .I like connecting with you") 


            elif "do you have here" in self.query:
                speak("I dont have hair,")  

            elif "do you ever go outside" in self.query:
                speak("“I love going outside. I don't have to worry about getting lost")                                

            elif "do you like to exercise" in self.query:
                speak("yaa i like to exercise")                            

            elif "do you have feeling" in self.query:
                speak("Do you have feelings")  
            elif "are you afraid of the dark" in self.query:
                speak("no i m not ")
             


























            ###################################################################################################################################
            ###########################################################################################################################################



            elif 'switch the window' in self.query:
                pyautogui.keyDown("alt")
                pyautogui.press("tab")
                time.sleep(1)
                pyautogui.keyUp("alt")
                    

            elif "tell me news" in self.query:
                speak("please wait sir, feteching the latest news")
                news()


            elif "Email to Aman" in self.query:
                
                speak("sir what should i say")
                self.query = self.takecommand()
                if "send a file" in self.query:
                    email = 't3021bca187@parulrsity.ac.in' # Your email
                    password = '7704003323Bcaunive' # Your email account password
                    send_to_email = input('amanpatwa234@gmail.com') # Whom you are sending the message to
                    speak("okay sir, what is the subject for this email")
                    self.query = self.takecommand()
                    subject = self.query   # The Subject in the email
                    speak("and sir, what is the message for this email")
                    self.query2 = self.takecommand()
                    message = self.query2  # The message in the email
                    speak("sir please enter the correct path of the file into the shell")
                    file_location = input("please enter the path")    # The File attachment in the email

                    speak("please wait,i am sending email now")

                    msg = MIMEMultipart()
                    msg['From'] = email
                    msg['To'] = send_to_email
                    msg['Subject'] = subject

                    msg.attach(MIMEText(message, 'plain'))

                    # Setup the attachment
                    filename = os.path.basename(file_location)
                    attachment = open(file_location, "rb")
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(attachment.read())
                    encoders.encode_base64(part)
                    part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

                    # Attach the attachment to the MIMEMultipart object
                    msg.attach(part)

                    server = smtplib.SMTP('smtp.gmail.com', 587)
                    server.starttls()
                    server.login(email, password)
                    text = msg.as_string()
                    server.sendmail(email, send_to_email, text)
                    server.quit()
                    speak("email has been sent to avinash")

                else:                
                    email = 't3021bca187@parulrsity.ac.in' # Your email
                    password = '7704003323Bca' # Your email account password
                    send_to_email = input("email address") # Whom you are sending the message to
                    message = self.query # The message in the email

                    server = smtplib.SMTP('smtp.gmail.com', 587) # Connect to the server
                    server.starttls() # Use TLS
                    server.login(email, password) # Login to the email server
                    server.sendmail(email, send_to_email , message) # Send the email
                    server.quit() # Logout of the email server
                    speak("email has been sent to avinash")


            ##########################################################################################################################################
            ###########################################################################################################################################

            elif "do some calculation" in self.query or "can you calculate" in self.query:            
                r = sr.Recognizer()
                with sr.Microphone() as source:
                    speak("Say what you want to calculate, example: 3 plus 3")
                    print("listening.....")
                    r.adjust_for_ambient_noise(source)
                    audio = r.listen(source)
                my_string=r.recognize_google(audio)
                print(my_string)
                def get_operator_fn(op):
                    return {
                        '+' : operator.add,
                        '-' : operator.sub,
                        'x' : operator.mul,
                        'divided' :operator.__truediv__,
                        'Mod' : operator.mod,
                        'mod' : operator.mod,
                        '^' : operator.xor,
                        }[op]
                def eval_binary_expr(op1, oper, op2):
                    op1,op2 = int(op1), int(op2)
                    return get_operator_fn(oper)(op1, op2)
                print(eval_binary_expr(*(my_string.split())))


            #-----------------To find my location using IP Address

            elif "where i am" in self.query or "where we are" in self.query:
                speak("wait sir, let me check")
                try:
                    ipAdd = requests.get('https://api.ipify.org').text
                    print(ipAdd)
                    url = 'https://get.geojs.io/v1/ip/geo/'+ipAdd+'.json'
                    geo_requests = requests.get(url)
                    geo_data = geo_requests.json()
                    # print(geo_data)
                    city = geo_data['city']
                    # state = geo_data['state']
                    country = geo_data['country']
                    speak(f"sir i am not sure, but i think we are in {city} city of {country} country")
                except Exception as e:
                    speak("sorry sir, Due to network issue i am not able to find where we are.")
                    pass


            

            #-------------------To check a instagram profile----
            elif "instagram profile" in  self.query or "profile on instagram" in self.query:
                speak("sir please enter the user name correctly.")
                name = input("Enter username here:")
                webbrowser.open(f"www.instagram.com/{name}")
                speak(f"Sir here is the profile of the user {name}")
                time.sleep(5)
                speak("sir would you like to download profile picture of this account.")
                condition = self.takecommand()
                if "yes" in condition:
                    mod = instaloader.Instaloader() #pip install instadownloader
                    mod.download_profile(name, profile_pic_only=True)
                    speak("i am done sir, profile picture is saved in our main folder. now i am ready for next command")
                else:
                    pass

            #-------------------  To take screenshot -------------
            elif "take screenshot" in self.query or "take a screenshot" in self.query:
                speak("sir, please tell me the name for this screenshot file")
                name = self.takecommand()
                speak("please sir hold the screen for few seconds, i am taking sreenshot")
                time.sleep(3)
                img = pyautogui.screenshot()
                img.save(f"{name}.png")
                speak("i am done sir, the screenshot is saved in our main folder. now i am ready for next command")



            #-------------------  To Read PDF file -------------
            elif "read pdf" in self.query:
                pdf_reader()

            #--------------------- To Hide files and folder ---------------
            elif "hide all files" in self.query or "hide this folder" in self.query or "visible for everyone" in self.query:
                speak("sir please tell me you want to hide this folder or make it visible for everyone")
                condition = self.takecommand()
                if "hide" in condition:
                    os.system("attrib +h /s /d") #os module
                    speak("sir, all the files in this folder are now hidden.")                

                elif "visible" in condition:
                    os.system("attrib -h /s /d")
                    speak("sir, all the files in this folder are now visible to everyone. i wish you are taking this decision in your own peace.")
                    
                elif "leave it" in condition or "leave for now" in condition:
                    speak("Ok sir")

            elif "temperature" in self.query:
                search = "weather in delhi"
                url = f"https://www.google.com/search?q={search}"
                req = requests.get(url)
                save = BeautifulSoup(req.text,"html.parser")
                tempp = save.find("div",class_= "BNeawe").text
                speak(f"current {search} is {tempp}")
            
            elif 'fine' in self.query or "good" in self.query:
              speak("It's good to know that your fine")

            elif "change my name to" in self.query:
                self.query = self.query.replace("change my name to", "")
                assname = self.query

            elif "change name" in self.query:
                speak("What would you like to call me, Sir ")
                assname = self.takecommand()
                speak("Thanks for naming me")

            elif "what's your name" in self.query or "what is your name" in self.query:
                speak("My friends call me")
                speak(assname)
                print("My friends call me", assname)

            elif 'exit' in self.query:
                speak("Thanks for giving me your time")
                exit()

            elif "who made you" in self.query or "who created you" in self.query:
                speak("I have been created by a groupp.")
                
            elif 'joke' in self.query:
                speak(pyjokes.get_joke())
                
            

            elif 'search' in self.query or 'search about' in self.query:
                
                self.query = self.query.replace("search about", "")
                self.query = self.query.replace("play", "")		
                webbrowser.open(self.query)

            elif "who i am" in self.query:
                speak("If you talk then definitely your human.")

            elif "why you came to world" in self.query:
                speak("Thanks to parul university. further It's a secret")

            elif ' openvoice assistant presentation' in self.query:
                speak("opening Power Point presentation")
                power = r"C:\\Users\\Urja\\OneDrive\\Desktop\\voice assistant.pptx"
                os.startfile(power)

            elif ' is love' in self.query:
                speak("It is 7th sense that destroy all other senses")

            elif "who are you" in self.query:
                speak("I am your virtual assistant created by a group ")

            elif 'reason for you' in self.query:
                speak("I was created as a Minor project by a group ")


            elif 'empty recycle bin' in self.query:
                winshell.recycle_bin().empty(confirm = False, show_progress = False, sound = True)
                speak("Recycle Bin Recycled")
            
            elif 'play music ' in self.query or 'gana bajao' in self.query or 'play some music' in self.query:
                speak("Here you go with music")
            # music_dir = "G:\\Song"
                music_dir = "C:\\New folder\\music file"
                songs = os.listdir(music_dir)
                print(songs)
                random = os.startfile(os.path.join(music_dir, songs[1]))

            elif "weather" in self.query:
                api_key="8ef61edcf1c576d65d836254e11ea420"
                base_url="https://api.openweathermap.org/data/2.5/weather?"
                speak("whats the city name")
                city_name=self.takecommand()
                complete_url=base_url+"appid="+api_key+"&q="+city_name
                response = requests.get(complete_url)
                x=response.json()
                if x["cod"]!="404":
                    y=x["main"]
                    current_temperature = y["temp"]
                    current_humidiy = y["humidity"]
                    z = x["weather"]
                    weather_description = z[0]["description"]
                    speak(" Temperature in kelvin unit is " +
                            str(current_temperature) +
                            "\n humidity in percentage is " +
                            str(current_humidiy) +
                            "\n description  " +
                            str(weather_description))
                    print(" Temperature in kelvin unit = " +
                         str(current_temperature) +
                         "\n humidity (in percentage) = " +
                         str(current_humidiy) +
                         "\n description = " +
                         str(weather_description))   

                         
                          

startExecution = MainThread()

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_jarvisUi()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.startTask)
        self.ui.pushButton_2.clicked.connect(self.close)

    def startTask(self):
        self.ui.movie = QtGui.QMovie("D:/background template.gif")
        self.ui.label.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie("D:/Jarvis_Loading_Screen.gif")
        self.ui.label_2.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie("D:/main_tem.gif")
        self.ui.label_3.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie("D:/new load.gif")
        self.ui.label_4.setMovie(self.ui.movie)
        self.ui.movie.start()
        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000)
        startExecution.start()

    def showTime(self):
        current_time = QTime.currentTime()
        current_date = QDate.currentDate()
        label_time = current_time.toString('hh:mm:ss')
        label_date = current_date.toString(Qt.ISODate)
        self.ui.textBrowser.setText(label_date)
        self.ui.textBrowser_2.setText(label_time)

#self.textBrowser.setText("Hello world")
 #       self.textBrowser.setAlignment(QtCore.Qt.AlignCenter)

app = QApplication(sys.argv)
jarvis = Main()
jarvis.show()
sys.exit(app.exec_())
