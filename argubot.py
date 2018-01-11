#! /usr/bin/env python

import speech_recognition as sr
import pyttsx
import ConfigParser
import sys
import argparse


class Argubot(object):  
    def __init__(self,lan="en"):
        self.cp = ConfigParser.ConfigParser()
        self.cp.read('./argubot.ini')
        self.lan = lan
        self.PYTTSX_RATE = self.cp.get('pyttsx','PYTTSX_RATE')
        self.PYTTSX_VOLUME = self.cp.get('pyttsx','PYTTSX_VOLUME')
        self.PYTTSX_VOICE = self.cp.get('pyttsx','PYTTSX_VOICE_'+self.lan ) 
        self.antonyms = dict(self.cp.items('antonyms '+ self.lan))
        #self.keyword_entries = []
        # for key in self.antonyms:
        #    self.keyword_entries.append((key, 1.0))

    def disagree(self):
        print "method is implemented in subclass"


    def __say(self, word):
        engine = pyttsx.init()
        engine.setProperty('rate', self.PYTTSX_RATE)
        engine.setProperty('volume', self.PYTTSX_VOLUME)
        engine.setProperty('voice', self.PYTTSX_VOICE)
        engine.say(word)
        engine.runAndWait()

    def __antonym(self, word):
        if self.antonyms.has_key(word):
            return self.antonyms[word]
        else:
            return False


if __name__ == "__main__":
    from argubot_snowboy import ArgubotSnowboy
    from argubot_wit import ArgubotWit
    ap = argparse.ArgumentParser(description="Wit.ai-based argubot")
    ap.add_argument("-l", "--lan", 
        required=False, 
        choices=["nl","en"],
        default="nl", 
        help="language (nl or en; defaults to en)")
    ap.add_argument("-t", "--type", 
        required=False, 
        choices=["wit","snowboy"],
        default="snowboy", 
        help="type of backend (wit or snowboy; defaults to snowboy)")

    args = vars(ap.parse_args())
    if args["type"]=="wit":
        argubot = ArgubotWit(lan=args["lan"])  
    else:
        argubot = ArgubotSnowboy(lan=args["lan"]) 
    argubot.disagree()

