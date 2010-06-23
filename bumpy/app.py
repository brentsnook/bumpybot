from waveapi import events
import bumpy

def Main():
    bumpy.Bumpy().run(OnRobotAdded)

def OnRobotAdded(event, wavelet):
    wavelet.reply("Sup? Pull features from: " + bumpy.Bumpy.pull_url(wavelet) + ", push them to " + bumpy.Bumpy.push_url(wavelet))