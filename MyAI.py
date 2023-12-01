import pyttsx3
import datetime
import pyaudio
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import smtplib
import playsound as ps
import multiprocessing
from bardapi import Bard
import re


# openai.api_key = "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"
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
# print(voices[3].id)
# 0 : DAVID, 1: KALPANA, 2 : HEMANT, 3 : ZIRA
def remove_bold(text):
    text = re.sub(r"^\*", "", text)
    text = re.sub(r"\*$", "", text)
    text = re.sub(r"\*", "", text)
    text = re.sub(r"\n", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text

# completion = openai.Completion()
# def Reply(question, model="gpt-3.5-turbo"):
#     prompt = question
#     response = openai.Completion.create(
#         model=model,
#         prompt=prompt,
#         max_tokens=100,
#         n=1,
#         stop=None,
#         temperature=0.5
#     )
#     answer = response.choices[0].text.strip()
#     return answer


language = "english"
if language == 'english':
    engine.setProperty('voice', voices[3].id)
elif language == 'hindi':
    engine.setProperty('voice', voices[1].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wishMe():
    if language == 'english':
        hour = int(datetime.datetime.now().hour)
        if hour >= 0 and hour < 12:
            speak('Good Morning Nimish')
        elif hour >= 12 and hour < 17:
            speak('Good Afternoon Nimish')
        else:
            speak('Good Evening Nimish')

        speak('What should I do for You...?')
    elif language == 'hindi':
        hour = int(datetime.datetime.now().hour)
        if hour >= 0 and hour < 12:
            speak('सुप्रभात निमिष')
        elif hour >= 12 and hour < 17:
            speak('शुभ दोपहर निमिष')
        else:
            speak('शुभ संध्या निमिष')

        speak('मैं आपकी किस प्रकार सहायता करूँ... ?')
        return


def takeCommand():
    # It takes microphone input from user and returns string output
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening...')
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print('Recognizing...')
        if language == 'english':
            query = r.recognize_google(audio, language='en-in')
        elif language == 'hindi':
            query = r.recognize_google(audio, language='hi')
        print('Instruction : ', query)

    except Exception as e:
        # print(e)
        print("Sorry I don't have any idea about it...")
        return
    return query


def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('sakalkalenimish@gmail.com', 'ksgeeacldprfapbd')
    server.sendmail('sakalkalenimish@gmail.com', to, content)
    server.close()


if __name__ == '__main__':
    wishMe()
    if 1:
        query = 'hello'  # takeCommand().casefold()
        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace('wikipedia', '')
            results = wikipedia.summary(query, sentences=2)
            speak('According to Wikipedia...')
            print(results)
            speak(results)

        elif 'open youtube' in query:
            speak('Opening Youtube')
            speak('What to search sir...?')
            search = takeCommand().casefold()
            searchq = str(search)
            speak('Ok Finding...')
            webbrowser.open(
                'https://www.youtube.com/results?search_query='+searchq)

        elif 'open google' in query:
            speak('Opening Google')
            speak('What to search sir...?')
            search = takeCommand().casefold()
            searchgoogle = str(search)
            speak('Ok Finding...')
            webbrowser.open('https://www.google.com/search?q='+searchgoogle)
        elif 'square root' in query:
            speak("Ok...")
            print('Enter The Number :')
            speak('Enter The Number ...')
            r = sr.Recognizer()
            with sr.Microphone() as source:
                r.pause_threshold = 1
                audio = r.listen(source)
                addcmnd = r.recognize_google(audio, language='en-in')
                sqno = (addcmnd)
                sqno = int(sqno.replace(" ", ""))
                sqrtno = sqno ** 0.5
                sqrtnostr = str(sqrtno)
                print(sqrtnostr)
                speak('The square root of the number entered by you is '+(sqrtnostr))

        elif 'addition' in query:
            speak('Ok Nimish...')
            speak('Enter First Number ...')
            r = sr.Recognizer()
            with sr.Microphone() as source:
                print('Enter First Number :')
                r.pause_threshold = 1
                audio = r.listen(source)
                addcmnd = r.recognize_google(audio, language='en-in')
                fno = int(addcmnd.replace(" ", ""))
                print(fno)
            speak('Enter Second Number ...')
            r = sr.Recognizer()
            with sr.Microphone() as source:
                print('Enter Second Number :')
                r.pause_threshold = 1
                audio = r.listen(source)
                addcmnd2 = r.recognize_google(audio, language='en-in')
                sno = int(addcmnd2)
                print(sno)
            result = fno+sno
            finalans = str(result)
            print('The answer is '+finalans)
            speak('The answer is '+finalans)
        elif 'time now' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak('Sir it is ' + strTime + ' currently')
        elif 'send email' in query:
            try:
                speak('To whom You Wanna Send the Mail?')
                toname = takeCommand().casefold()
                print(toname)
                speak('What should I send Sir ... ?')
                content = takeCommand().casefold()
                if toname == 'nimish':
                    to = 'sakalkalenimish@gmail.com'
                sendEmail(to, content)
                speak('Email has been successfully sent to ' +
                      (toname.capitalize())+' ...')
                print('Email has been successfully sent to ' +
                      (toname.capitalize())+' ...')
            except Exception as e:
                print(e)
                speak("Couldn't send the email sir...")
        elif 'play music' in query:
            speak('Which song to play...?')
            song = takeCommand().casefold()
            if song == 'faded':
                p = multiprocessing.Process(target=ps.playsound, args=(
                    "C:/Users/Owner/Downloads/Faded.mp3",))
                p.start()
                input("press ENTER to stop playback")
                p.terminate()
            elif song == 'alone':
                p = multiprocessing.Process(target=ps.playsound, args=(
                    "C:/Users/Owner/Downloads/Alone.mp3",))
                p.start()
                input("press ENTER to stop playback")
                p.terminate()
        elif 'bye' in query:
            speak('Bye... Nimish Have A Good Day...')
        else:
            response = Bard(token='dQh6ZDwlj47FX11uVK92SR1dVdAGNURdLHedSY_dqkFjdVWJYf3Y_dVls5OW_x_DG7jOuQ.').get_answer(
                str(query)+" in 3 lines")['content']
            output = remove_bold(response)
            print(output)
            speak(output)
