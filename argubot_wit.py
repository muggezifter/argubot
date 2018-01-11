#! /usr/bin/env python

import speech_recognition as sr
import pyttsx
import ConfigParser
import sys
import argparse
from argubot import Argubot

class ArgubotWit(Argubot):  
    def __init__(self,lan="en"):
        super(ArgubotWit,self).__init__(lan=lan)
        self.WIT_AI_KEY = self.cp.get('api keys','WIT_AI_KEY')

    def disagree(self):
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
                        self.say("argubot wins another argument")
                        exit()
                    print("Wit.ai thinks you said '" + word + "'")
                    ant = self.__antonym(word)
                    if ant:
                        print "If you say '" + word + "' I say '" + ant + "'"
                        self.__say(ant)
            except sr.UnknownValueError:
                print("Wit.ai could not understand audio")
            except sr.RequestError as e:
                print("Could not request results from Wit.ai service; {0}".format(e))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Wit.ai-based argubot")
    ap.add_argument("-l", "--lan", 
        required=False, 
        choices=["nl","en"],
        default="en", 
        help="language (nl or en; defaults to en)")
    args = vars(ap.parse_args())
    arglan = args["lan"]
    argubot = ArgubotWit(lan=arglan)
    argubot.disagree()
