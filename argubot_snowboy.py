#! /usr/bin/env python
import argubot 
import argparse
import os.path
import os
import snowboydecoder
import sys
import signal


class ArgubotSnowboy(argubot.Argubot):
    def __init__(self, lan="en"):
        super(ArgubotSnowboy,self).__init__(lan=lan)
        self.model_path = self.cp.get('snowboy','model_path')
        self.models = []
        self.callbacks = []
        self.cnt = 0
        for key in self.antonyms:
            if os.path.isfile(self.model_path + key + ".pmdl"):
                self.models.append(self.model_path + key + ".pmdl") 
                self.callbacks.append(lambda ant=self.antonyms[key]: self.say(ant))

    def disagree(self):
    	global signal
    	global interrupted 
    	interrupted = False
        signal.signal(signal.SIGINT, self.signal_handler)
        self.create_detector()


    def create_detector(self):
        sensitivity = [0.5]*len(self.models)
        self.detector = snowboydecoder.HotwordDetector(self.models, sensitivity=sensitivity)
        print('Listening... Press Ctrl+C to exit')

        self.detector.start(detected_callback=self.callbacks,
                interrupt_check=self.interrupt_callback,
                sleep_time=0.3)

    def say(self, word):
         self.detector.terminate()
         os.system("espeak -v" + self.PYTTSX_VOICE + "+f2 -s" + self.PYTTSX_RATE + " " + word )
         self.create_detector()

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
        help="language (nl or en; defaults to nl)")
    args = vars(ap.parse_args())
    arglan = args["lan"]
    argubot = ArgubotSnowboy(lan=arglan)
    argubot.disagree()