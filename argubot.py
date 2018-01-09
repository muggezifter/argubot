#! /usr/bin/env python

import speech_recognition as sr
import pyttsx
import ConfigParser
import sys


Config = ConfigParser.ConfigParser()
Config.read('./argubot.ini')
WIT_AI_KEY = Config.get('api keys','WIT_AI_KEY')
PYTTSX_RATE = Config.get('pyttsx','PYTTSX_RATE')
PYTTSX_VOLUME = Config.get('pyttsx','PYTTSX_VOLUME')
PYTTSX_VOICE = Config.get('pyttsx','PYTTSX_VOICE') 
antonyms = dict(Config.items('antonyms'))
keyword_entries = []
for key in antonyms:
    keyword_entries.append((key, 1.0))


def say(s):
    engine = pyttsx.init()
    engine.setProperty('rate', PYTTSX_RATE)
    engine.setProperty('volume', PYTTSX_VOLUME)
    engine.setProperty('voice', PYTTSX_VOICE)
    engine.say(s)
    a = engine.runAndWait()

def antonym(word):
    if antonyms.has_key(word):
        return antonyms[word]
    else:
        return False

def main(argv):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print ("adjusting for ambient noise...")
        r.adjust_for_ambient_noise(source)
    while True: 
        with sr.Microphone() as source:
            print("Say something!")
            audio = r.listen(source,)
            print "retrieving from Wit.ai...."
        try:
            w = r.recognize_wit(audio, key=WIT_AI_KEY)
            words = w.split(' ')
            for word in words:
                if word == 'stop':
                    print "bye"
                    break;
                print("Wit.ai thinks you said '" + word + "'")
                ant = antonym(word)
                if ant:
                    print "If you say '" + word + "' I say '" + ant + "'"
                    say(ant)
        except sr.UnknownValueError:
            print("Wit.ai could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Wit.ai service; {0}".format(e))
    exit()

if __name__ == "__main__":
    main(sys.argv[1:])
