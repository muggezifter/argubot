#! /usr/bin/env python

from argubot import Argubot
import speech_recognition as sr
import pyttsx
import ConfigParser
import sys

class ArgubotSnowboy(Argubot):
    def __init__(self):
       super(ArgubotSnowboy,self).__init__()

if __name__ == "__main__":
    argubot = ArgubotSnowboy()
    argubot.disagree(sys.argv[1:])