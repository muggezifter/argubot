#! /usr/bin/env python
from argubot import Argubot
import argparse
import os.path
import pyttsx
import snowboydecoder
import sys
import signal


class ArgubotSnowboy(Argubot):
    def __init__(self, lan="en"):
        super(ArgubotSnowboy,self).__init__(lan=lan)
        self.model_path = self.cp.get('snowboy','model_path')
        self.models = []
        self.callbacks = []
        
        self.callbacks.extend([lambda: self.__say("rechts")])
        self.callbacks.extend([lambda: self.__say("links")])
        self.callbacks.extend([lambda: self.__say("ja")])
        self.callbacks.extend([lambda: self.__say("zwart")])
        self.callbacks.extend([lambda: self.__say("wit")])
        self.callbacks.extend([lambda: self.__say("goed")])
        self.callbacks.extend([lambda: self.__say("nee")])

        for key in self.antonyms:
            self.models.append(self.model_path + key + ".pmdl")
			#self.callbacks.extend([lambda x: self.__self.antonyms[key]])
        print self.callbacks 
        print self.PYTTSX_VOICE
    def disagree(self):
    	global signal
    	global interrupted 
    	interrupted = False
        signal.signal(signal.SIGINT, self.signal_handler)

        sensitivity = [0.5]*len(self.models)
        detector = snowboydecoder.HotwordDetector(self.models, sensitivity=sensitivity)
        print('Listening... Press Ctrl+C to exit')

        # main loop
        # make sure you have the same numbers of callbacks and models
        detector.start(detected_callback=self.callbacks,
                interrupt_check=self.interrupt_callback,
                sleep_time=0.03)

        detector.terminate()

    def __say(self, word):
        engine = pyttsx.init()
        engine.setProperty('rate', self.PYTTSX_RATE)
        engine.setProperty('volume', self.PYTTSX_VOLUME)
        engine.setProperty('voice', self.PYTTSX_VOICE)
        engine.say(word)
        engine.runAndWait()

    def signal_handler(self, signal, frame):
        global interrupted
        interrupted = True
    def interrupt_callback(self):
    	global interrupted
        return interrupted

if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Snowboy-based argubot")
    ap.add_argument("-l", "--lan", 
        required=False, 
        choices=["nl","en"],
        default="nl", 
        help="language (nl or en; defaults to en)")
    args = vars(ap.parse_args())
    arglan = args["lan"]
    argubot = ArgubotSnowboy(lan=arglan)
    argubot.disagree()