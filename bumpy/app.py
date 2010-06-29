from waveapi import events
from bumpy import Bumpy

def Main():
    Bumpy().run(OnRobotAdded)

def OnRobotAdded(event, wavelet):
    wavelet.reply("Sup? Pull features from: " + Bumpy.pull_url(wavelet) + ", push them to " + Bumpy.push_url(wavelet))