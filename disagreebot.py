#! /usr/bin/env python

import speech_recognition as sr
import pyttsx
import ConfigParser


antonyms = {
    "yes" : "no",
    "no" : "yes",
    "left" : "right",
    "right" : "left",
    "up" : "down",
    "down" : "up",
    'black' : 'white',
    'white' : 'black',
    'in' : 'out',
    'out' : 'in',
    'dark' : 'light',
    'light' : 'dark',
    'good' : 'bad'
}


def say(s):
    engine = pyttsx.init()
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate-50)
    volume = engine.getProperty('volume')
    engine.setProperty('volume', volume-0.80)
    engine.setProperty('voice', 'english-us')
    engine.say(s)
    a = engine.runAndWait()

def antonym(word):
    if antonyms.has_key(word):
        return antonyms[word]
    else:
        return False


Config = ConfigParser.ConfigParser()
Config.read('./disagreebot.ini')
WIT_AI_KEY = Config.get('api keys','wit_ai_key') 

r = sr.Recognizer()
while True: 
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)
        print "retrieving from Wit.ai...."
    try:
        w = r.recognize_wit(audio, key=WIT_AI_KEY)
        words = w.split(' ')
        for word in words:
            if word == 'stop':
                print "bye"
                break;
            print("Wit.ai thinks you said '" + word + "'")
            a = antonym(word)
            if a:
                print "If you say '" + word + "' I say '" + a + "'"
                say(a)
        
    except sr.UnknownValueError:
        print("Wit.ai could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Wit.ai service; {0}".format(e))
