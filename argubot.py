#! /usr/bin/env python

import speech_recognition as sr
import pyttsx
import ConfigParser
import sys


class Argubot:  
    def __init__(self):
        Config = ConfigParser.ConfigParser()
        Config.read('./argubot.ini')
        self.WIT_AI_KEY = Config.get('api keys','WIT_AI_KEY')
        self.PYTTSX_RATE = Config.get('pyttsx','PYTTSX_RATE')
        self.PYTTSX_VOLUME = Config.get('pyttsx','PYTTSX_VOLUME')
        self.PYTTSX_VOICE = Config.get('pyttsx','PYTTSX_VOICE') 
        self.antonyms = dict(Config.items('antonyms'))
        self.keyword_entries = []
        for key in self.antonyms:
            self.keyword_entries.append((key, 1.0))

    def disagree(self, argv):
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
                w = r.recognize_wit(audio, key=self.WIT_AI_KEY)
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

    def say(self, word):
        engine = pyttsx.init()
        engine.setProperty('rate', self.PYTTSX_RATE)
        engine.setProperty('volume', self.PYTTSX_VOLUME)
        engine.setProperty('voice', self.PYTTSX_VOICE)
        engine.say(word)
        _ = engine.runAndWait()

    def antonym(self, word):
        if self.antonyms.has_key(word):
            return self.antonyms[word]
        else:
            return False


if __name__ == "__main__":
    argubot = Argubot()
    argubot.disagree(sys.argv[1:])
