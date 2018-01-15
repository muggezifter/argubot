#! /usr/bin/env python
import argubot 
import argparse
import os.path
import os
import snowboydecoder
import sys
import signal
import time

class ArgubotSnowboy(argubot.Argubot):
    def __init__(self, lan="en"):
        super(ArgubotSnowboy,self).__init__(lan=lan)
        self.model_path = self.cp.get('snowboy','model_path')
        self.models = []
        self.callbacks = []
        self.cnt = 0
        self.interrupted = False
        self.signal = signal
        self.signal.signal(self.signal.SIGINT, self.signal_handler)
        for key in self.antonyms:
            if os.path.isfile(self.model_path + key + ".pmdl"):
                self.models.append(self.model_path + key + ".pmdl") 
                self.callbacks.append(lambda ant=self.antonyms[key]: self.say(ant))

    def disagree(self):
        print("ARGUBOT v.0.2.1")
        print("[python version, engine: snowboy]")
        sensitivity = [0.5]*len(self.models)
        self.detector = snowboydecoder.HotwordDetector(self.models, sensitivity=sensitivity)
        print('listening... press ctrl+c to exit')
        self.detector.start(detected_callback=self.callbacks,
                interrupt_check=self.interrupt_callback,
                sleep_time=0.3)
        self.detector.terminate()

    def say(self, word):
        if not self.speaking:
            self.speaking = True
            os.system("espeak -v" + self.PYTTSX_VOICE + "+m2 -s" + self.PYTTSX_RATE + " " + word )
            time.sleep(2)
            self.speaking = False

    def signal_handler(self, signal, frame):
        self.interrupted = True

    def interrupt_callback(self):
        if self.interrupted:
            print(" ARGUBOT signing off")
        return self.interrupted

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
